"""File processing operations for translation"""

import logging
import os
from pathlib import Path

# Configure logging to write to a file in the project root
log_file = Path(__file__).parent.parent.parent.parent / "transphrase.log"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Test logging configuration
logger = logging.getLogger("file_processor")
logger.debug("Logging configuration test - this should appear in transphrase.log")

import datetime
import logging
import os
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, TaskID

from transphrase.api.handler import APIHandler

# Add these imports at the top
from transphrase.core.config import (
    HTML_POLISH_PROMPT_TEMPLATE,
    HTML_TRANSLATION_PROMPT_TEMPLATE,
    LANGUAGE_SPECIFIC_POLISH,
    POLISH_STYLE_PRESETS,
    TranslationConfig,
)
from transphrase.core.context_tracker import ContextTracker
from transphrase.core.db.db_operations import DatabaseOperations
from transphrase.core.processing.chunk_processor import ChunkProcessor
from transphrase.core.processing.file_handlers import FileHandlers
from transphrase.core.processing.html_processor import HTMLProcessor
from transphrase.core.processing.progress_tracker import ProgressTracker
from transphrase.core.quality.quality_assessor import QualityAssessor
from transphrase.core.utils.language_detector import LanguageDetector
from transphrase.database.models import DBManager

logger = logging.getLogger("translator")
console = Console()


class FileProcessor:
    """Handles file processing operations for translation"""

    # Class attribute for supported extensions
    SUPPORTED_EXTENSIONS = [".txt", ".html"]

    def __init__(
        self,
        config: TranslationConfig,
        api_handler: APIHandler,
        db_manager: Optional[DBManager] = None,
    ):
        """
        Initialize file processor

        Args:
            config: Translation configuration
            api_handler: API handler for translation
            db_manager: Database manager instance
        """
        # Add config validation and debug logging
        if config is None:
            logger.error("Received None config in FileProcessor initialization")
            raise ValueError("Configuration cannot be None")

        logger.debug(f"Initializing FileProcessor with config: {config}")
        logger.debug(f"Config type: {type(config)}")
        logger.debug(f"Config has source_language: {hasattr(config, 'source_language')}")
        logger.debug(f"Config has target_language: {hasattr(config, 'target_language')}")

        self.config = config
        self.api_handler = api_handler
        self.db_manager = db_manager  # Store db_manager as an instance attribute
        self.db_operations = DatabaseOperations(db_manager)
        self.language_detector = LanguageDetector()
        self.quality_assessor = QualityAssessor()
        self.file_handlers = FileHandlers(config, db_manager)
        self.chunk_processor = ChunkProcessor(config, api_handler)
        self.progress_tracker = ProgressTracker()
        self.html_processor = HTMLProcessor()
        self.context_tracker = None
        self.results_lock = threading.Lock()
        self.chunk_count_lock = threading.Lock()

    def detect_language(self, text: str, min_length: int = 100) -> Optional[str]:
        """
        Detect the language of the given text.

        Args:
            text: Text to analyze
            min_length: Minimum text length for reliable detection

        Returns:
            Language name or None if detection fails
        """
        return self.language_detector.detect(text, min_length)

    def detect_files_language(
        self, files: List[Path], sample_size: int = 5, text_sample_bytes: int = 3000
    ) -> Optional[str]:
        """
        Detect the dominant language across multiple files.

        Args:
            files: List of files to sample
            sample_size: Number of files to sample
            text_sample_bytes: Number of bytes to read from each file

        Returns:
            Detected language name or None if detection fails
        """
        return self.language_detector.detect_files_language(files, sample_size, text_sample_bytes)

    def find_processable_files(self) -> List[Path]:
        """
        Find all processable files in source directory.

        Returns:
            List of paths to processable files
        """
        file_info = self.file_handlers.find_text_files()
        return [item["path"] for item in file_info]

    def _prepare_work_items(
        self, files: List[Path], job_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Prepare and prioritize work items for better load balancing."""
        # Convert file paths to file info format expected by file_handlers
        files_to_process = []
        for file in files:
            try:
                file_size = file.stat().st_size
            except OSError:
                file_size = 0

            files_to_process.append({"path": file, "size": file_size, "priority": 0})

        return self.file_handlers._prepare_work_items(files_to_process, job_id)

    def _process_chunk(
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
        return self.chunk_processor.process_chunk(
            chunk, system_prompt, model, progress, chunk_task_id
        )

    def _split_text(self, text: str) -> List[str]:
        """
        Split text into appropriate chunks for processing.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        return self.chunk_processor.split_text(text)

    def _create_file_record(self, job_id: str, source_path: str, output_path: str) -> None:
        """Create file record in database"""
        self.file_handlers._create_file_record(job_id, source_path, output_path)

    def _update_file_status(
        self,
        job_id: str,
        source_path: str,
        status: str,
        error: str = None,
        quality_score: float = None,
    ) -> None:
        """
        Update file status in database and increment completed files counter

        Args:
            job_id: Job ID
            source_path: Source file path
            status: Status (completed, failed, skipped)
            error: Optional error message
            quality_score: Optional quality score
        """
        self.file_handlers._update_file_status(job_id, source_path, status, error, quality_score)

    def _assess_quality(self, source_text: str, translated_text: str) -> float:
        """
        Assess the quality of a translation.

        Args:
            source_text: Original text
            translated_text: Translated text

        Returns:
            Quality score between 0-10
        """
        return self.quality_assessor.assess_quality(source_text, translated_text)

    def _calculate_quality_metrics(
        self, chunk_scores: List[float], full_source: str, full_target: str
    ) -> Dict[str, float]:
        """
        Calculate overall quality metrics from chunk scores and full text.

        Args:
            chunk_scores: Quality scores for individual chunks
            full_source: Complete source text
            full_target: Complete translated text

        Returns:
            Dictionary of quality metrics
        """
        return self.quality_assessor.calculate_quality_metrics(
            chunk_scores, full_source, full_target
        )

    def _get_quality_label(self, score: float) -> str:
        """
        Get a human-readable label for a quality score.

        Args:
            score: Quality score (0-10)

        Returns:
            Quality label
        """
        return self.quality_assessor.get_quality_label(score)

    def _get_optimal_worker_count(self) -> int:
        """
        Calculate the optimal number of worker threads based on system and job characteristics.

        Returns:
            Optimal number of worker threads
        """
        import os

        cpu_count = os.cpu_count() or 4

        # Default to CPU count minus 1 but at least 1
        workers = max(1, cpu_count - 1)

        # Allow override from config
        if hasattr(self.config, "max_workers") and self.config.max_workers:
            workers = min(workers, self.config.max_workers)

        return workers

    def process_files(self) -> None:
        """Process all files for translation or polishing with optimized parallelism."""
        from transphrase.core.config_validator import ConfigurationValidator

        # Validate configuration using the centralized validator
        if not ConfigurationValidator.validate_config(self.config):
            console.print("[red]Invalid configuration detected![/red]")
            logger.error("Configuration validation failed")
            return

        # Get safe config values
        config_values = ConfigurationValidator.get_safe_config_values(self.config)
        logger.debug(f"Using config values: {config_values}")

        # Update config with safe values
        for key, value in config_values.items():
            setattr(self.config, key, value)

        # Find all files to process
        processable_files = self.find_processable_files()
        total_files = len(processable_files)

        if total_files == 0:
            console.print("[yellow]No processable files found in source directory.[/yellow]")
            console.print(
                f"[yellow]Supported formats: {', '.join(self.SUPPORTED_EXTENSIONS)}[/yellow]"
            )
            return

        # Debug: Verify config exists before language detection
        if not hasattr(self, "config") or self.config is None:
            console.print("[red]Configuration is missing before language detection![/red]")
            logger.error("Config is None before language detection")
            return

        logger.debug(f"Config before language detection: {self.config}")
        logger.debug(f"Config has source_language: {hasattr(self.config, 'source_language')}")
        logger.debug(
            f"Config has auto_detect_language: {hasattr(self.config, 'auto_detect_language')}"
        )

        # Auto-detect source language if not specified
        if not self.config.source_language and self.config.auto_detect_language:
            detected_language = self.detect_files_language(processable_files)
            if detected_language:
                self.config.source_language = detected_language
                console.print(f"[green]Auto-detected source language: {detected_language}[/green]")
                logger.debug(f"Set source_language to: {detected_language}")
            else:
                console.print(
                    "[yellow]Could not automatically detect language. Please specify source language.[/yellow]"
                )
                logger.warning("Failed to auto-detect language")
                return
        elif not self.config.source_language:
            console.print(
                "[yellow]Source language not specified and auto-detection disabled.[/yellow]"
            )
            logger.warning("Source language not specified and auto-detection disabled")
            return

        # Debug: Verify config after language detection
        if not hasattr(self, "config") or self.config is None:
            console.print("[red]Configuration was lost after language detection![/red]")
            logger.error("Config is None after language detection")
            return

        # Verify config is still valid after detection
        if not hasattr(self, "config") or self.config is None:
            console.print("[red]Configuration was lost after language detection![/red]")
            return

        # Debug: Log config state
        logger.debug(f"Config after language detection: {self.config}")
        logger.debug(f"Source language: {self.config.source_language}")
        logger.debug(f"Target language: {self.config.target_language}")

        # Create job record if database is available
        job_id = None
        if self.db_manager:
            job_id = self.db_operations.create_job_record(
                source_dir=str(self.config.source_dir),
                output_dir=str(self.config.output_dir),
                model_id=self.config.model,
                system_prompt=self.config.system_prompt,
                source_language=self.config.source_language,
                target_language=self.config.target_language,
                total_files=total_files,
            )

        # Initialize context tracker with job information
        if self.config.use_context_cache:
            self.context_tracker = ContextTracker(
                job_id=job_id,
                source_language=self.config.source_language,
                target_language=self.config.target_language,
                model=self.config.model,
                series_id=self.config.series_id,
            )

        # Load glossary terms if series ID is provided
        if self.config.series_id and hasattr(self.api_handler, "cache"):
            logger.info(f"Loading glossary terms for series: {self.config.series_id}")
            if hasattr(self.api_handler.cache, "load_series_glossary"):
                self.api_handler.cache.load_series_glossary(self.config.series_id)

        # Show appropriate message based on mode
        mode_message = "Polishing" if self.config.mode == "polish" else "Translating"

        # Get optimized worker count
        worker_count = self._get_optimal_worker_count()

        # Modify this part to include polish style information
        if self.config.mode == "polish":
            console.print(
                f"[bold green]Processing {total_files} files with {worker_count} workers\n"
                f"{mode_message}: {self.config.source_language} → {self.config.target_language}\n"
                f"Polish style: {self.config.polish_style}\n"
                f"Using model: {self.config.model}[/bold green]"
            )
        else:
            console.print(
                f"[bold green]Processing {total_files} files with {worker_count} workers\n"
                f"{mode_message}: {self.config.source_language} → {self.config.target_language}\n"
                f"Using model: {self.config.model}[/bold green]"
            )

        # Prepare work items with prioritization
        work_items = self._prepare_work_items(processable_files, job_id)

        # Estimate total chunks for progress tracking
        total_chunks = self.file_handlers.estimate_total_chunks(
            work_items, self.config.max_chunk_size
        )

        # Initialize progress tracking
        self.progress_tracker.initialize(total_files, total_chunks)

        # Process files in parallel with optimized worker count
        results = self.process_files_in_parallel(
            work_items, self.config.system_prompt, self.config.model, self.progress_tracker, job_id
        )

        # Finalize progress tracking
        self.progress_tracker.finalize()

        # Update job status if database is available
        if self.db_manager and job_id:
            self.db_operations.update_job_status(job_id, "completed")

        # Display quality summary
        quality_data = {path: metrics for path, _, metrics in results if metrics}
        if quality_data:
            self.quality_assessor.display_quality_summary(quality_data)

        # Show files that might need review
        self.quality_assessor.display_review_files(quality_data)

        # Display processing statistics
        self.progress_tracker.display_statistics()

        console.print("\n[bold green]✨ Translation completed successfully! ✨[/bold green]")

    def process_files_in_parallel(
        self,
        work_items: List[Dict[str, Any]],
        system_prompt: str,
        model: str,
        progress: Progress,  # This is a Progress object, not a ProgressTracker
        job_id: Optional[str] = None,
        files_task_id: Optional[TaskID] = None,
        chunks_task_id: Optional[TaskID] = None,
        current_file_task_id: Optional[TaskID] = None,
    ) -> List[Tuple[Path, str, Optional[Dict[str, float]]]]:
        """
        Process files in parallel, with special handling for HTML files

        Args:
            work_items: List of work items to process
            system_prompt: System prompt for translation
            model: Model to use
            progress: Progress instance for tracking progress
            job_id: Optional job ID
            files_task_id: Optional task ID for files progress
            chunks_task_id: Optional task ID for chunks progress
            current_file_task_id: Optional task ID for current file progress

        Returns:
            List of tuples with (output_path, result, quality_metrics)
        """
        results = []

        # Use provided task IDs or create new ones if not provided
        if files_task_id is None:
            files_task_id = progress.add_task("[cyan]Files", total=len(work_items))

        if chunks_task_id is None:
            # Estimate total chunks if not provided
            total_chunks = sum(
                max(1, item.get("size", 0) // self.config.max_chunk_size) for item in work_items
            )
            chunks_task_id = progress.add_task("[green]Chunks", total=total_chunks)

        if current_file_task_id is None:
            current_file_task_id = progress.add_task("[yellow]Current file", visible=False)

        # Prepare file status dictionary for progress tracking
        file_status = {str(item["path"]): {"chunks": 0, "total_chunks": 0} for item in work_items}
        active_files = set()

        # Determine optimal worker count based on system and configuration
        worker_count = self._get_optimal_worker_count()

        # Process files with ThreadPoolExecutor for parallelism
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            # Create partial function for process_file_optimized with fixed parameters
            from functools import partial

            process_func = partial(
                self._process_single_file,
                system_prompt=system_prompt,
                model=model,
                progress=progress,
                chunks_task_id=chunks_task_id,
                current_file_task_id=current_file_task_id,
                file_status=file_status,
                active_files=active_files,
                job_id=job_id,
            )

            # Submit all work items
            future_to_item = {executor.submit(process_func, item): item for item in work_items}

            # Process completed files as they finish
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)

                    # Update file progress
                    progress.update(files_task_id, advance=1)

                    # Calculate and update ETA
                    if (
                        hasattr(self.progress_tracker, "total_chunks_processed")
                        and self.progress_tracker.total_chunks_processed > 0
                    ):
                        elapsed = time.time() - self.progress_tracker.start_time
                        total_chunks = sum(stats["total_chunks"] for stats in file_status.values())
                        remaining_chunks = (
                            total_chunks - self.progress_tracker.total_chunks_processed
                        )

                        if elapsed > 0:
                            rate = self.progress_tracker.total_chunks_processed / elapsed
                            eta_seconds = remaining_chunks / rate if rate > 0 else 0
                            eta = datetime.timedelta(seconds=int(eta_seconds))

                            # Update ETA display if there's an eta_task
                            if hasattr(self.progress_tracker, "eta_task"):
                                progress.update(
                                    self.progress_tracker.eta_task,
                                    description=f"[magenta]ETA: {eta}",
                                    visible=True,
                                )

                except Exception as e:
                    logger.error(f"Error processing {item['path']}: {e}")
                    # Update file progress even on error
                    progress.update(files_task_id, advance=1)

        return results

    def _process_single_file(
        self,
        item: Dict[str, Any],
        system_prompt: str,
        model: str,
        progress: Progress,
        chunks_task_id: TaskID,
        current_file_task_id: TaskID,
        file_status: Dict[str, Dict[str, int]],
        active_files: set,
        job_id: Optional[str] = None,
    ) -> Optional[Tuple[Path, str, Dict[str, float]]]:
        """
        Process a single file with optimized handling for different file types.

        Args:
            item: Work item with file path and metadata
            system_prompt: System prompt for translation
            model: Model to use
            progress: Progress tracker instance
            chunks_task_id: Task ID for chunks progress
            current_file_task_id: Task ID for current file progress
            file_status: Dictionary tracking file processing status
            active_files: Set of currently active files
            job_id: Optional job ID

        Returns:
            Tuple of (output_path, result_content, quality_metrics) or None if processing failed
        """
        source_path = item["path"]
        file_path_str = str(source_path)
        file_name = source_path.name
        file_ext = source_path.suffix.lower()

        # Update active files for display
        with self.results_lock:
            active_files.add(file_path_str)
            progress.update(
                current_file_task_id, description=f"[yellow]Processing: {file_name}", visible=True
            )

        try:
            # Read file content
            with open(source_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            # Create output directory if it doesn't exist
            output_dir = self.config.output_dir
            output_dir.mkdir(parents=True, exist_ok=True)

            # Create output path
            output_path = output_dir / file_name

            # Create file record in database if job_id is provided
            if job_id:
                self._create_file_record(job_id, str(source_path), str(output_path))

            # Calculate expected chunks for this file
            chunks = self._split_text(content)
            total_file_chunks = len(chunks)

            # Update file status for progress tracking
            file_status[file_path_str]["total_chunks"] = total_file_chunks

            # Log processing start
            logger.info(
                f"Processing file: {file_name} ({len(content) / 1024:.1f}KB, {total_file_chunks} chunks)"
            )

            # Verify config is still valid before processing
            if not hasattr(self, "config") or self.config is None:
                logger.error("Configuration was lost before file processing!")
                return None

            # Debug: Log config state
            logger.debug(f"Config before processing {file_name}: {self.config}")
            logger.debug(f"Source language: {self.config.source_language}")
            logger.debug(f"Target language: {self.config.target_language}")

            # Process based on file type
            start_time = time.time()
            if file_ext == ".html":
                # Process HTML file
                processed_content, quality_metrics = self._process_html_file(
                    content, system_prompt, model, self.progress_tracker
                )
            else:
                # Process text file
                processed_content, quality_metrics = self._process_text_file(
                    content, system_prompt, model, self.progress_tracker
                )

            # Write processed content to output file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(processed_content)

            # Calculate processing time and speed
            processing_time = time.time() - start_time
            processing_speed = len(content) / processing_time if processing_time > 0 else 0

            # Log completion
            logger.info(
                f"Completed file: {file_name} in {processing_time:.2f}s "
                f"({processing_speed / 1024:.1f}KB/s)"
            )

            # Update file status in database
            if job_id:
                self._update_file_status(
                    job_id, str(source_path), "completed", quality_score=quality_metrics["overall"]
                )

            return output_path, processed_content, quality_metrics

        except Exception as e:
            # Log error
            error_msg = f"Error processing {file_name}: {str(e)}"
            logger.error(error_msg)

            # Update file status in database
            if job_id:
                self._update_file_status(job_id, str(source_path), "failed", error=str(e))

            return None

        finally:
            # Remove file from active files
            with self.results_lock:
                active_files.discard(file_path_str)

                # Show next file in progress if available, or hide current file display
                if active_files:
                    next_active = next(iter(active_files))
                    progress.update(
                        current_file_task_id,
                        description=f"[yellow]Processing: {Path(next_active).name}",
                        visible=True,
                    )
                else:
                    progress.update(current_file_task_id, visible=False)

    def _process_html_file(
        self, content: str, system_prompt: str, model: str, progress_tracker: ProgressTracker
    ) -> Tuple[str, Dict[str, float]]:
        # Add comprehensive config validation with detailed error handling
        if not hasattr(self, "config") or self.config is None:
            logger.error("Configuration is missing in _process_html_file")
            logger.debug("Stack trace:", exc_info=True)
            raise ValueError("Configuration is required for HTML processing")

        # Ensure required config attributes exist with detailed logging
        required_attrs = ["source_language", "target_language", "mode"]
        missing_attrs = [attr for attr in required_attrs if not hasattr(self.config, attr)]

        if missing_attrs:
            logger.error(f"Missing required config attributes: {missing_attrs}")
            logger.debug(f"Current config state: {self.config}")
            raise ValueError(f"Configuration missing required attributes: {missing_attrs}")

        # Create safe access to config attributes with fallback values
        source_lang = getattr(self.config, "source_language", "auto-detected")
        target_lang = getattr(self.config, "target_language", "English")
        mode = getattr(self.config, "mode", "translate")

        logger.debug(
            f"Using config values - source_language: {source_lang}, target_language: {target_lang}, mode: {mode}"
        )
        """
        Process HTML file content with improved structure preservation and performance

        Args:
            content: HTML content
            system_prompt: System prompt for translation
            model: Model to use
            progress_tracker: Progress tracker instance

        Returns:
            Tuple of (processed HTML content, quality metrics)
        """
        # Choose optimal processing strategy based on file size
        large_file_threshold = 50000  # 50KB

        # For large files, use the optimized large file processor
        if len(content) > large_file_threshold:
            return self._process_large_html_file(content, system_prompt, model, progress_tracker)

        # Add comprehensive null checks for config and its attributes
        logger.debug(f"Config in _process_html_file: {self.config}")
        logger.debug(f"Config type: {type(self.config)}")
        logger.debug(f"Config has source_language: {hasattr(self.config, 'source_language')}")

        if not hasattr(self, "config") or self.config is None:
            # Use system_prompt directly if config is not available
            html_prompt = system_prompt
            logger.warning(
                "Configuration not available for HTML processing, using default system prompt"
            )
        else:
            # Use specialized HTML prompts from config.py with safe attribute access
            mode = getattr(self.config, "mode", "translate")
            source_lang = getattr(self.config, "source_language", "auto-detected")
            target_lang = getattr(self.config, "target_language", "English")

            logger.debug(f"Mode: {mode}, Source: {source_lang}, Target: {target_lang}")

            if mode == "translate":
                try:
                    html_prompt = HTML_TRANSLATION_PROMPT_TEMPLATE.format(
                        source_language=source_lang, target_language=target_lang
                    )
                    logger.debug(f"HTML prompt: {html_prompt}")
                except Exception as e:
                    logger.error(f"Error formatting HTML prompt: {e}")
                    html_prompt = system_prompt
            else:
                html_prompt = system_prompt

        # Create a translation function with enhanced context handling and caching
        def translate_html_content(text):
            # Skip translation for empty or whitespace-only content
            if not text.strip():
                return text

            # Enhance prompt with context if available
            enhanced_prompt = html_prompt
            if self.context_tracker:
                try:
                    enhanced_prompt = self.context_tracker.get_enhanced_prompt(html_prompt, text)
                except AttributeError as e:
                    logger.warning(f"Error enhancing prompt: {e}. Using original prompt.")
                    # Continue with original prompt

            # Use cached result if available (even if context_tracker is not used)
            if hasattr(self.api_handler, "cache") and self.api_handler.cache:
                try:
                    cached_result = self.api_handler.cache.get(text, enhanced_prompt, model)
                    if cached_result:
                        # Don't increment progress counter for cached results
                        return cached_result
                except Exception as e:
                    logger.warning(f"Cache lookup failed: {e}. Proceeding with direct translation.")

            # Translate the text
            result = self.api_handler.translate_chunk(enhanced_prompt, text, model)

            # Update context tracker with null check
            if self.context_tracker:
                try:
                    self.context_tracker.update_context(text, result)
                except AttributeError as e:
                    logger.warning(f"Failed to update context: {e}")

            # Update progress
            with self.chunk_count_lock:
                progress_tracker.total_chunks_processed += 1

            return result

        # Use the structure-preserving translation method
        start_time = time.time()
        result = self.html_processor.translate_html_with_protection(content, translate_html_content)

        # Log processing time for performance analysis
        processing_time = time.time() - start_time
        logger.debug(f"HTML processing took {processing_time:.3f}s for {len(content)/1024:.1f}KB")

        # Simple quality assessment
        quality_score = self.quality_assessor._assess_quality(content[:1000], result[:1000])
        quality_metrics = {
            "overall": quality_score,
            "fluency": min(1.0, quality_score * 1.1),
            "consistency": min(1.0, quality_score * 0.9),
            "processing_time": processing_time,
        }

        return result, quality_metrics

    def _process_large_html_file(
        self, content: str, system_prompt: str, model: str, progress_tracker: ProgressTracker
    ) -> Tuple[str, Dict[str, float]]:
        # Add a check to ensure self.config is not None
        if not hasattr(self, "config") or self.config is None:
            # Use system_prompt directly if config is not available
            html_prompt = system_prompt
            logger.warning(
                "Configuration not available for HTML processing, using default system prompt"
            )
        else:
            # Use specialized HTML prompt
            if getattr(self.config, "mode", "translate") == "translate":
                # Fix: Check for null values and provide defaults before formatting
                source_lang = "auto-detected"
                target_lang = "English"

                if hasattr(self.config, "source_language") and self.config.source_language:
                    source_lang = self.config.source_language

                if hasattr(self.config, "target_language") and self.config.target_language:
                    target_lang = self.config.target_language

                html_prompt = HTML_TRANSLATION_PROMPT_TEMPLATE.format(
                    source_language=source_lang, target_language=target_lang
                )

        # Continue with the rest of the function...
        logger.info(f"Processing large HTML file ({len(content)/1024:.1f}KB) in chunks")

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".html", mode="w", encoding="utf-8"
        ) as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name

        # Create a callback function for the streaming processor
        quality_scores = []

        def translate_callback(segments_batch: List[str]) -> List[str]:

            results = []
            for segment in segments_batch:
                if not segment.strip():
                    results.append(segment)
                    continue

                # Get enhanced prompt if context tracker is available
                enhanced_prompt = html_prompt
                if self.context_tracker:
                    enhanced_prompt = self.context_tracker.get_enhanced_prompt(html_prompt, segment)

                # Translate segment
                translated = self.api_handler.translate_chunk(enhanced_prompt, segment, model)
                results.append(translated)

                # Track quality
                quality = self.quality_assessor._assess_quality(segment, translated)
                quality_scores.append(quality)

                # Update context
                if self.context_tracker:
                    self.context_tracker.update_context(segment, translated)

                # Update progress
                with self.chunk_count_lock:
                    progress_tracker.total_chunks_processed += 1

            return results

        # Process the file in chunks
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".html", mode="w", encoding="utf-8"
        ) as out_file:
            output_path = out_file.name

        try:
            # Process file in chunks
            result = self.html_processor.process_large_html(
                tmp_path, translate_callback, max_chunk_size=100000, output_path=output_path
            )

            # Read the processed content
            with open(output_path, "r", encoding="utf-8") as f:
                processed_content = f.read()

            # Calculate quality metrics
            avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
            quality_metrics = {
                "overall": avg_quality,
                "fluency": min(1.0, avg_quality * 1.1),  # Estimate metrics
                "consistency": min(1.0, avg_quality * 0.9),
                "samples": len(quality_scores),
            }

            return processed_content, quality_metrics

        finally:
            # Clean up temporary files
            try:
                os.unlink(tmp_path)
                os.unlink(output_path)
            except Exception as e:
                logger.warning(f"Failed to clean up temporary files: {e}")

    def _process_text_file(
        self, content: str, system_prompt: str, model: str, progress_tracker: ProgressTracker
    ) -> Tuple[str, Dict[str, float]]:
        """
        Process text file content with batch processing for improved performance

        Args:
            content: Text content
            system_prompt: System prompt for translation
            model: Model to use
            progress_tracker: Progress tracker instance

        Returns:
            Tuple of (processed text content, quality metrics)
        """
        # Split into chunks
        chunks = self._split_text(content)

        # For very short content, process directly
        if len(chunks) <= 1:
            processed_chunk = self.api_handler.translate_chunk(system_prompt, content, model)
            quality_score = self.quality_assessor._assess_quality(content, processed_chunk)

            quality_metrics = {
                "overall": quality_score,
                "fluency": min(1.0, quality_score * 1.1),
                "consistency": min(1.0, quality_score * 0.9),
            }

            return processed_chunk, quality_metrics

        # Process chunks in batches for better throughput
        batch_size = min(5, max(1, len(chunks) // 4))  # Dynamic batch size
        processed_chunks = []
        quality_scores = []

        # Process chunks in batches
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            non_empty_batch = [chunk for chunk in batch if chunk.strip()]
            empty_indices = [j for j, chunk in enumerate(batch) if not chunk.strip()]

            if not non_empty_batch:
                # If batch is all empty, just add empty chunks
                processed_chunks.extend(batch)
                continue

            # Enhanced prompts with context
            enhanced_prompts = []
            for chunk in non_empty_batch:
                prompt = system_prompt
                if self.context_tracker:
                    prompt = self.context_tracker.get_enhanced_prompt(system_prompt, chunk)
                enhanced_prompts.append(prompt)

            # If all prompts are the same, use batch translation
            if len(set(enhanced_prompts)) == 1:
                # Use batch translation API
                if hasattr(self.api_handler, "translate_batch"):
                    processed_batch = self.api_handler.translate_batch(
                        enhanced_prompts[0], non_empty_batch, model
                    )
                else:
                    # Fall back to individual translations
                    processed_batch = []
                    for chunk in non_empty_batch:
                        translated = self.api_handler.translate_chunk(
                            enhanced_prompts[0], chunk, model
                        )
                        processed_batch.append(translated)
            else:
                # Process each chunk individually when contexts differ
                processed_batch = []
                for j, chunk in enumerate(non_empty_batch):
                    translated = self.api_handler.translate_chunk(enhanced_prompts[j], chunk, model)
                    processed_batch.append(translated)

            # Update context for each chunk
            if self.context_tracker:
                for j, (chunk, processed) in enumerate(zip(non_empty_batch, processed_batch)):
                    self.context_tracker.update_context(chunk, processed)

            # Calculate quality scores
            for j, (chunk, processed) in enumerate(zip(non_empty_batch, processed_batch)):
                score = self.quality_assessor._assess_quality(chunk, processed)
                quality_scores.append(score)

            # Reassemble batch with empty chunks
            full_processed_batch = []
            non_empty_idx = 0

            for j in range(len(batch)):
                if j in empty_indices:
                    full_processed_batch.append(batch[j])  # Keep empty chunks unchanged
                else:
                    full_processed_batch.append(processed_batch[non_empty_idx])
                    non_empty_idx += 1

            processed_chunks.extend(full_processed_batch)

            # Update progress
            with self.chunk_count_lock:
                progress_tracker.total_chunks_processed += len(non_empty_batch)

        # Join processed chunks
        result = "".join(processed_chunks)

        # Calculate quality metrics
        quality_metrics = self.quality_assessor._calculate_quality_metrics(
            quality_scores, content, result
        )

        return result, quality_metrics
