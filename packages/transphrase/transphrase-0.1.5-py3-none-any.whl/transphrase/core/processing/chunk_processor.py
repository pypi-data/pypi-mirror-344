"""Chunk processing operations for translation"""

import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from rich.progress import Progress, TaskID

from transphrase.api.handler import APIHandler
from transphrase.core.config import TranslationConfig
from transphrase.core.context_tracker import ContextTracker
from transphrase.core.processing.text_processor import TextProcessor
from transphrase.formats.html.html_protection import StructureProtector

logger = logging.getLogger("translator")


class ChunkProcessor:
    """Handles processing of text chunks"""

    def __init__(
        self,
        config: TranslationConfig,
        api_handler: APIHandler,
        context_tracker: Optional[ContextTracker] = None,
    ):
        """
        Initialize chunk processor

        Args:
            config: Translation configuration
            api_handler: API handler for translation
            context_tracker: Context tracker instance
        """
        self.config = config
        self.api_handler = api_handler
        self.context_tracker = context_tracker
        # Initialize thread safety and progress tracking
        self.chunk_count_lock = threading.Lock()
        self.total_chunks_processed = 0
        self.html_protector = StructureProtector()
        self.text_processor = TextProcessor(api_handler)

    def process_chunk(
        self, chunk: str, system_prompt: str, model: str, progress: Progress, chunk_task_id: TaskID
    ) -> str:
        """
        Process a single chunk of text.

        Args:
            chunk: Text chunk to process
            system_prompt: System prompt for translation
            model: Model to use for translation
            progress: Progress tracker instance
            chunk_task_id: Task ID for progress tracking

        Returns:
            Processed text chunk
        """
        # Skip empty chunks
        if not chunk.strip():
            return chunk

        # Enhance prompt with context if available
        enhanced_prompt = system_prompt
        if self.context_tracker:
            enhanced_prompt = self.context_tracker.get_enhanced_prompt(system_prompt, chunk)

        # Use cached result if available
        if hasattr(self.api_handler, "cache") and self.api_handler.cache:
            cached_result = self.api_handler.cache.get(chunk, enhanced_prompt, model)
            if cached_result:
                return cached_result

        # Translate the chunk
        result = self.api_handler.translate_chunk(enhanced_prompt, chunk, model)

        # Update context tracker
        if self.context_tracker:
            self.context_tracker.update_context(chunk, result)

        # Update progress
        with self.chunk_count_lock:
            self.total_chunks_processed += 1
            progress.update(chunk_task_id, completed=self.total_chunks_processed)

        return result

    def split_text(self, text: str) -> List[str]:
        """
        Split text into appropriate chunks for processing.

        Uses semantic splitting to preserve coherence of paragraphs and sections.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        return self.text_processor.split_text_semantic(
            text,
            max_chunk_size=self.config.max_chunk_size,
        )

    def process_files_in_parallel(
        self,
        work_items: List[Dict[str, Any]],
        system_prompt: str,
        model: str,
        progress_tracker: Progress,
        job_id: Optional[str] = None,
    ) -> List[Tuple[Path, str, Optional[Dict[str, float]]]]:
        """
        Process files in parallel, with special handling for HTML files

        Args:
            work_items: List of work items to process
            system_prompt: System prompt for translation
            model: Model to use
            progress_tracker: Progress tracker instance
            job_id: Optional job ID

        Returns:
            List of tuples with (output_path, result, quality_metrics)
        """
        results = []
        files_task_id = progress_tracker.add_task("Processing files", total=len(work_items))
        chunks_task_id = progress_tracker.add_task(
            "Processing chunks", total=100
        )  # Will update later

        # Determine optimal worker count based on system and configuration
        max_workers = self.config.max_workers if hasattr(self.config, "max_workers") else 4
        worker_count = min(max(1, max_workers), len(work_items))

        # Process files with ThreadPoolExecutor for parallelism
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            # Create future-to-item mapping
            future_to_item = {}

            # Submit all work items to the executor
            for item in work_items:
                future = executor.submit(
                    self._process_single_file,
                    item,
                    system_prompt,
                    model,
                    progress_tracker,
                    chunks_task_id,
                    job_id,
                )
                future_to_item[future] = item

            # Process completed futures as they come in
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    output_path, result, quality_metrics = future.result()
                    results.append((output_path, result, quality_metrics))

                    # Update progress
                    progress_tracker.update_task(files_task_id)

                except Exception as exc:
                    logger.error(f"File {item['path']} generated an exception: {exc}")
                    results.append((item.get("out_path", item["path"]), None, None))
                    progress_tracker.update_task(files_task_id)

        return results

    def _process_single_file(
        self,
        work_item: Dict[str, Any],
        system_prompt: str,
        model: str,
        progress_tracker: Progress,
        chunks_task_id: TaskID,
        job_id: Optional[str] = None,
    ) -> Tuple[Path, str, Dict[str, float]]:
        """
        Process a single file with appropriate handling based on file type

        Args:
            work_item: Work item dictionary with file information
            system_prompt: System prompt for translation
            model: Model to use
            progress_tracker: Progress tracker instance
            chunks_task_id: Task ID for chunks progress
            job_id: Optional job ID

        Returns:
            Tuple of (output_path, processed_content, quality_metrics)
        """
        path = work_item["path"]
        out_path = work_item.get("out_path", Path(str(path) + ".translated"))

        # Ensure output directory exists
        out_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Read the file content
            content = path.read_text(encoding="utf-8")

            # Process based on file type
            if path.suffix.lower() == ".html":
                result, quality_metrics = self._process_html_content(
                    content, system_prompt, model, progress_tracker, chunks_task_id
                )
            else:
                result, quality_metrics = self._process_text_content(
                    content, system_prompt, model, progress_tracker, chunks_task_id
                )

            # Write result to file
            out_path.write_text(result, encoding="utf-8")

            return out_path, result, quality_metrics

        except Exception as e:
            logger.exception(f"Error processing file {path}: {str(e)}")
            raise

    def _process_html_content(
        self,
        content: str,
        system_prompt: str,
        model: str,
        progress_tracker: Progress,
        chunks_task_id: TaskID,
    ) -> Tuple[str, Dict[str, float]]:
        """
        Process HTML content with structure preservation

        Args:
            content: HTML content
            system_prompt: System prompt for translation
            model: Model to use
            progress_tracker: Progress tracker instance
            chunks_task_id: Task ID for chunks progress

        Returns:
            Tuple of (processed HTML content, quality metrics)
        """
        start_time = time.time()
        quality_scores = []

        def translate_func(text):
            # Skip empty text
            if not text.strip():
                return text

            # Enhance prompt with context if available
            enhanced_prompt = system_prompt
            if self.context_tracker:
                enhanced_prompt = self.context_tracker.get_enhanced_prompt(system_prompt, text)

            # Use cached result if available
            if hasattr(self.api_handler, "cache") and self.api_handler.cache:
                cached_result = self.api_handler.cache.get(text, enhanced_prompt, model)
                if cached_result:
                    return cached_result

            # Translate the text
            result = self.api_handler.translate_chunk(enhanced_prompt, text, model)

            # Calculate quality if text is long enough
            if len(text) > 30 and len(result) > 30:
                from transphrase.core.quality.quality_assessor import assess_quality

                score = assess_quality(text, result)
                quality_scores.append(score)

            # Update context tracker
            if self.context_tracker:
                self.context_tracker.update_context(text, result)

            # Update progress
            with self.chunk_count_lock:
                self.total_chunks_processed += 1
                progress_tracker.update(chunks_task_id, completed=self.total_chunks_processed)

            return result

        # Use HTML protector to translate while preserving structure
        result = self.html_protector.translate_with_protection(content, translate_func)

        # Calculate processing time
        processing_time = time.time() - start_time

        # Calculate quality metrics
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        quality_metrics = {
            "overall": avg_quality,
            "fluency": min(1.0, avg_quality * 1.1),  # Estimated fluency
            "consistency": min(1.0, avg_quality * 0.9),  # Estimated consistency
            "processing_time": processing_time,
            "samples": len(quality_scores),
        }

        return result, quality_metrics

    def _process_text_content(
        self,
        content: str,
        system_prompt: str,
        model: str,
        progress_tracker: Progress,
        chunks_task_id: TaskID,
    ) -> Tuple[str, Dict[str, float]]:
        """
        Process plain text content with chunk-based translation

        Args:
            content: Text content
            system_prompt: System prompt for translation
            model: Model to use
            progress_tracker: Progress tracker instance
            chunks_task_id: Task ID for chunks progress

        Returns:
            Tuple of (processed text content, quality metrics)
        """
        # For very short content, process directly
        if len(content) < self.config.max_chunk_size:
            processed_content = self.process_chunk(
                content, system_prompt, model, progress_tracker, chunks_task_id
            )

            # Calculate simple quality metrics
            from transphrase.core.quality.quality_assessor import assess_quality

            quality_score = assess_quality(content, processed_content)
            quality_metrics = {
                "overall": quality_score,
                "fluency": min(1.0, quality_score * 1.1),
                "consistency": min(1.0, quality_score * 0.9),
            }

            return processed_content, quality_metrics

        # For longer content, split into chunks
        chunks = self.split_text(content)
        processed_chunks = []
        quality_scores = []

        # Update progress task with actual chunk count
        progress_tracker.update(chunks_task_id, total=len(chunks))

        # Process each chunk
        for chunk in chunks:
            processed_chunk = self.process_chunk(
                chunk, system_prompt, model, progress_tracker, chunks_task_id
            )
            processed_chunks.append(processed_chunk)

            # Calculate quality for this chunk
            from transphrase.core.quality.quality_assessor import assess_quality

            quality_score = assess_quality(chunk, processed_chunk)
            quality_scores.append(quality_score)

        # Join processed chunks
        result = "".join(processed_chunks)

        # Calculate overall quality metrics
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        quality_metrics = {
            "overall": avg_quality,
            "fluency": min(1.0, avg_quality * 1.1),
            "consistency": min(1.0, avg_quality * 0.9),
            "samples": len(quality_scores),
        }

        return result, quality_metrics
