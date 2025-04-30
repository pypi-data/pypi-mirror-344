"""File processing operations for translation"""

import datetime
import logging
import os
import threading
import time
import uuid
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from langdetect import LangDetectException, detect
from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from transphrase.api.handler import APIHandler
from transphrase.core.config import MAX_CHUNK_SIZE, TranslationConfig
from transphrase.core.context_tracker import ContextTracker
from transphrase.core.text_processing import split_text_semantic
from transphrase.database.models import DBManager, TranslationFile, TranslationJob

logger = logging.getLogger("translator")
console = Console()


class FileProcessor:
    """Handles file processing operations for translation"""

    # Language code mapping from ISO 639-1 to human-readable names
    LANGUAGE_CODES = {
        "en": "English",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ru": "Russian",
        "pt": "Portuguese",
        "it": "Italian",
        "ar": "Arabic",
        "hi": "Hindi",
        "vi": "Vietnamese",
        "th": "Thai",
        "id": "Indonesian",
    }

    # Quality score thresholds
    QUALITY_THRESHOLDS = {
        "excellent": 9.0,
        "good": 7.5,
        "acceptable": 6.0,
        "needs_review": 4.0,
    }

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
        self.config = config
        self.api_handler = api_handler
        self.db_manager = db_manager
        self.context_tracker = None  # Will be initialized in process_files
        self.results_lock = threading.Lock()
        self.chunk_count_lock = threading.Lock()
        self.total_chunks_processed = 0
        # Quality assessment tracking
        self.quality_scores = {}

    def detect_language(self, text: str, min_length: int = 100) -> Optional[str]:
        """
        Detect the language of the given text.

        Args:
            text: Text to analyze
            min_length: Minimum text length for reliable detection

        Returns:
            Language name or None if detection fails
        """
        # If text is too short, detection may be unreliable
        if len(text) < min_length:
            logger.debug(f"Text too short for reliable language detection: {len(text)} chars")
            return None

        try:
            lang_code = detect(text)
            # Convert ISO code to language name if available
            return self.LANGUAGE_CODES.get(lang_code, lang_code)
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {e}")
            return None

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
        if not files:
            return None

        # Sample a subset of files
        sample_files = files[: min(sample_size, len(files))]
        detected_languages = []

        for file_path in sample_files:
            try:
                # Read a portion of the file
                text = file_path.read_text(encoding="utf-8", errors="ignore")
                sample_text = text[:text_sample_bytes]

                lang = self.detect_language(sample_text)
                if lang:
                    detected_languages.append(lang)
                    logger.debug(f"Detected {lang} in {file_path.name}")
            except Exception as e:
                logger.error(f"Error reading file {file_path} for language detection: {e}")

        # Use most common detected language
        if detected_languages:
            most_common_lang = Counter(detected_languages).most_common(1)[0][0]
            logger.info(f"Auto-detected source language: {most_common_lang}")
            return most_common_lang

        return None

    def find_text_files(self) -> List[Path]:
        """
        Find all text files in source directory

        Returns:
            List of paths to text files
        """
        return sorted(self.config.source_dir.rglob("*.txt"))

    def _get_optimal_worker_count(self) -> int:
        """Determine optimal worker count based on system resources and rate limits"""
        worker_count = self.config.workers

        # Reduce worker count if rate limits have been hit
        if hasattr(self.api_handler, "rate_limiter") and self.api_handler.rate_limiter:
            if self.api_handler.rate_limiter.actual_rate_limits_detected:
                worker_count = min(2, worker_count)
                logger.info(f"Rate limits detected, reducing worker count to {worker_count}")

        # Consider available CPU cores
        cpu_count = os.cpu_count() or 4
        if worker_count > cpu_count * 2:
            new_count = cpu_count * 2
            logger.info(
                f"Optimizing worker count from {worker_count} to {new_count} based on available CPUs"
            )
            worker_count = new_count

        # Ensure at least one worker
        return max(1, worker_count)

    def _prepare_work_items(
        self, txt_files: List[Path], job_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Prepare and prioritize work items for better load balancing"""
        work_items = []

        for path in txt_files:
            rel = path.relative_to(self.config.source_dir)
            out_path = self.config.output_dir / rel

            # Skip existing files if configured
            if self.config.skip_existing and out_path.with_suffix(".txt").exists():
                logger.info(f"🔶 Skipping existing: {rel}")

                # Update database if available
                if self.db_manager and job_id:
                    self._update_file_status(job_id, str(rel), "skipped")

                continue

            # Create file record in database if available
            if self.db_manager and job_id:
                self._create_file_record(job_id, str(rel), str(out_path))

            # Get file size for sorting
            try:
                file_size = path.stat().st_size
            except OSError:
                file_size = 0

            work_items.append(
                {"path": path, "rel_path": rel, "out_path": out_path, "size": file_size}
            )

        # Sort by file size (largest first) for better load balancing
        return sorted(work_items, key=lambda x: x["size"], reverse=True)

    def _process_chunk(
        self, chunk: str, system_prompt: str, model: str, progress: Progress, chunk_task_id: TaskID
    ) -> str:
        """Process a single chunk of text"""
        result = self.api_handler.translate_chunk(system_prompt, chunk, model)

        # Update progress
        with self.chunk_count_lock:
            self.total_chunks_processed += 1
            progress.update(chunk_task_id, completed=self.total_chunks_processed)

        return result

    def _split_text(self, text: str) -> List[str]:
        """
        Split text into appropriate chunks for processing.

        Uses semantic splitting to preserve coherence of paragraphs and sections.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        # Import is at the top of the file, but used here:
        # from transphrase.core.text_processing import split_text_semantic

        # Delegate to the imported semantic splitter
        return split_text_semantic(
            text,
            max_chunk_size=self.config.max_chunk_size,
        )

    def process_file_optimized(
        self,
        work_item: Dict[str, Any],
        progress: Progress,
        file_task_id: TaskID,
        chunk_task_id: TaskID,
        current_file_task_id: TaskID,
        file_status: Dict[str, Dict[str, int]],
        active_files: set,
        job_id: Optional[str] = None,
    ) -> Optional[Tuple[Path, str, Dict[str, float]]]:
        """
        Process a single file with optimized chunking and parallelism

        Args:
            work_item: Dictionary containing file information
            progress: Progress bar instance
            file_task_id: Task ID for file progress
            chunk_task_id: Task ID for chunk progress
            current_file_task_id: Task ID for current file progress
            file_status: Dictionary tracking per-file progress
            active_files: Set of currently active files
            job_id: Optional job ID for database

        Returns:
            Tuple of (output_path, result, quality_metrics) or None on failure
        """
        path = work_item["path"]
        rel_path = work_item["rel_path"]
        out_path = work_item["out_path"]
        file_path_str = str(path)

        # Add to active files set
        active_files.add(file_path_str)

        # Update current file progress display
        progress.update(
            current_file_task_id, description=f"[yellow]Current: {path.name}", visible=True
        )

        try:
            # Read the text file
            text = path.read_text(encoding="utf-8")

            # Tell context tracker we're starting a new file
            if self.context_tracker:
                self.context_tracker.start_file(path)

            mode = self.config.mode

            # Initialize result
            result = ""
            # Track quality metrics for chunks
            chunk_quality_scores = []

            # For small files, process directly
            if len(text) <= self.config.max_chunk_size:
                # Track file chunks
                file_status[file_path_str]["total_chunks"] = 1

                enhanced_prompt = self.config.system_prompt
                if self.context_tracker:
                    enhanced_prompt = self.context_tracker.get_enhanced_prompt(
                        self.config.system_prompt, text
                    )

                # Process start time for chunk
                chunk_start = time.time()

                result = self.api_handler.translate_chunk(enhanced_prompt, text, self.config.model)

                # Calculate and store processing rate
                chunk_time = time.time() - chunk_start
                processing_rate = len(text) / chunk_time if chunk_time > 0 else 0
                self.processed_chunks_rate.append(processing_rate)

                # Assess quality of translation
                quality_score = self._assess_quality(text, result)
                chunk_quality_scores.append(quality_score)

                # Update context with processed text
                if self.context_tracker:
                    self.context_tracker.update_context(text, result)

                # Update chunk progress
                with self.chunk_count_lock:
                    self.total_chunks_processed += 1
                    file_status[file_path_str]["chunks"] += 1
                    progress.update(chunk_task_id, completed=self.total_chunks_processed)
            else:
                # For large files, split into chunks
                chunks = self._split_text(text)
                processed_chunks = []

                # Update file status
                file_status[file_path_str]["total_chunks"] = len(chunks)

                # Create file-specific progress display
                file_progress_desc = f"[cyan]File: {path.name}"
                file_progress_id = progress.add_task(
                    file_progress_desc, total=len(chunks), visible=True
                )

                # Add quality tracking task
                quality_task_id = progress.add_task(
                    f"[blue]Quality", visible=True, total=10, completed=0  # Scale from 0-10
                )

                # Process chunks sequentially to maintain context
                for i, chunk in enumerate(chunks):
                    enhanced_prompt = self.config.system_prompt
                    if self.context_tracker:
                        enhanced_prompt = self.context_tracker.get_enhanced_prompt(
                            self.config.system_prompt, chunk
                        )

                    # Process start time for chunk
                    chunk_start = time.time()

                    processed_chunk = self.api_handler.translate_chunk(
                        enhanced_prompt, chunk, self.config.model
                    )

                    # Calculate and store processing rate
                    chunk_time = time.time() - chunk_start
                    processing_rate = len(chunk) / chunk_time if chunk_time > 0 else 0
                    self.processed_chunks_rate.append(processing_rate)

                    # Assess quality of translation
                    quality_score = self._assess_quality(chunk, processed_chunk)
                    chunk_quality_scores.append(quality_score)

                    # Update quality display (average of current chunks)
                    current_avg_quality = sum(chunk_quality_scores) / len(chunk_quality_scores)
                    quality_label = self._get_quality_label(current_avg_quality)
                    progress.update(
                        quality_task_id,
                        completed=current_avg_quality,
                        description=f"[blue]Quality: {current_avg_quality:.2f}/10 ({quality_label})",
                    )

                    processed_chunks.append(processed_chunk)

                    # Update context with processed chunk
                    if self.context_tracker:
                        self.context_tracker.update_context(chunk, processed_chunk)

                    # Update chunk progress
                    with self.chunk_count_lock:
                        self.total_chunks_processed += 1
                        file_status[file_path_str]["chunks"] += 1
                        progress.update(chunk_task_id, completed=self.total_chunks_processed)
                        progress.update(file_progress_id, completed=i + 1)

                result = "\n".join(processed_chunks)
                # Remove file-specific progress when done
                progress.remove_task(file_progress_id)
                progress.remove_task(quality_task_id)

            # Apply processor plugins if configured
            if hasattr(self.config, "plugins") and self.config.plugins.get("processors"):
                from transphrase.plugins.plugin_manager import PluginManager

                plugin_manager = PluginManager()

                for processor_name in self.config.plugins["processors"]:
                    processor_class = plugin_manager.get_processor_module(processor_name)
                    if processor_class:
                        try:
                            processor = processor_class()
                            result = processor.process_text(result)
                            logger.info(f"Applied processor: {processor_name}")
                        except Exception as e:
                            logger.error(f"Error applying processor '{processor_name}': {e}")

            # Calculate final quality metrics
            quality_metrics = self._calculate_quality_metrics(chunk_quality_scores, text, result)

            # Store quality score for reporting
            self.quality_scores[str(path)] = quality_metrics

            # Add quality assessment to log message
            quality_label = self._get_quality_label(quality_metrics["overall"])

            # Log success - use different terminology for polish vs translate
            if mode == "polish":
                logger.info(
                    f"✅ Polished: {os.path.relpath(path, Path.cwd())} -> "
                    f"{os.path.relpath(out_path, Path.cwd())} "
                    f"Quality: {quality_metrics['overall']:.2f}/10 ({quality_label})"
                )
            else:
                logger.info(
                    f"✅ Translated: {os.path.relpath(path, Path.cwd())} -> "
                    f"{os.path.relpath(out_path, Path.cwd())} "
                    f"Quality: {quality_metrics['overall']:.2f}/10 ({quality_label})"
                )

            # Update database if available - mark as completed and store quality metrics
            if self.db_manager and job_id:
                self._update_file_status(
                    job_id, str(rel_path), "completed", quality_score=quality_metrics["overall"]
                )

            return out_path, result, quality_metrics

        except Exception as e:
            # Log error
            logger.error(f"❌ Failed: {os.path.relpath(path, Path.cwd())} - {e}")

            # Update database with error if available
            if self.db_manager and job_id:
                self._update_file_status(job_id, str(rel_path), "failed", error=str(e))

            return None
        finally:
            # Update file progress
            progress.update(file_task_id, advance=1)

            # Remove from active files
            active_files.discard(file_path_str)

    def _assess_quality(self, source_text: str, translated_text: str) -> float:
        """
        Assess the quality of a translation using various metrics.

        Args:
            source_text: Original text
            translated_text: Translated text

        Returns:
            Quality score between 0-10
        """
        # Initialize scoring components
        scores = {
            "length_ratio": 0.0,  # How reasonable is the length ratio between source and target
            "formatting": 0.0,  # Preservation of formatting elements
            "entity_preservation": 0.0,  # Preservation of named entities, numbers, etc.
            "fluency": 0.0,  # Basic fluency checks
        }

        # 1. Length ratio check (penalize translations that are too short or too long)
        source_len = len(source_text)
        target_len = len(translated_text)

        if source_len > 0 and target_len > 0:
            ratio = target_len / source_len

            # Calculate ideal ratio based on language pair
            ideal_ratio = self._get_ideal_length_ratio(
                self.config.source_language, self.config.target_language
            )

            # Score based on how close to ideal ratio
            ratio_diff = abs(ratio - ideal_ratio)
            if ratio_diff < 0.2:
                scores["length_ratio"] = 10.0  # Very close to ideal
            elif ratio_diff < 0.5:
                scores["length_ratio"] = 8.0  # Somewhat close
            elif ratio_diff < 1.0:
                scores["length_ratio"] = 6.0  # Acceptable
            else:
                scores["length_ratio"] = 3.0  # Significantly off

        # 2. Formatting preservation
        # Check for similar paragraph structure
        source_paragraphs = source_text.count("\n\n")
        target_paragraphs = translated_text.count("\n\n")

        if source_paragraphs == 0:
            # If no paragraphs, score is perfect
            scores["formatting"] = 10.0
        else:
            para_diff = abs(source_paragraphs - target_paragraphs)
            if para_diff == 0:
                scores["formatting"] = 10.0
            elif para_diff <= 2:
                scores["formatting"] = 8.0
            elif para_diff <= 5:
                scores["formatting"] = 6.0
            else:
                scores["formatting"] = 4.0

        # 3. Entity preservation (basic check for numbers)
        source_numbers = set("".join(c for c in source_text if c.isdigit()))
        target_numbers = set("".join(c for c in translated_text if c.isdigit()))

        if not source_numbers:
            # If no numbers in source, score is perfect
            scores["entity_preservation"] = 10.0
        else:
            # Score based on number preservation
            common_digits = len(source_numbers.intersection(target_numbers))
            total_digits = len(source_numbers)

            if total_digits > 0:
                scores["entity_preservation"] = (common_digits / total_digits) * 10.0
            else:
                scores["entity_preservation"] = 10.0

        # 4. Basic fluency check (no repetitions, reasonable sentence length)
        # Check for obvious repetitions
        repetition_score = 10.0
        words = translated_text.split()
        if len(words) >= 6:  # Only check substantial text
            # Look for 3-word repetitions
            for i in range(len(words) - 5):
                trigram = " ".join(words[i : i + 3])
                if trigram in " ".join(words[i + 3 : i + 6]):
                    repetition_score -= 3.0
                    break

        # Check sentence length distribution
        sentences = [
            s.strip()
            for s in translated_text.replace("!", ".").replace("?", ".").split(".")
            if s.strip()
        ]
        if sentences:
            avg_sent_len = sum(len(s) for s in sentences) / len(sentences)
            if avg_sent_len > 300:
                # Excessively long sentences are penalized
                sentence_score = 5.0
            elif avg_sent_len < 10 and len(sentences) > 3:
                # Excessively short sentences are penalized (if there are multiple)
                sentence_score = 7.0
            else:
                sentence_score = 10.0

            scores["fluency"] = (repetition_score + sentence_score) / 2
        else:
            scores["fluency"] = repetition_score

        # Calculate weighted average
        weights = {
            "length_ratio": 0.25,
            "formatting": 0.25,
            "entity_preservation": 0.25,
            "fluency": 0.25,
        }

        weighted_score = sum(scores[k] * weights[k] for k in scores)

        # Ensure score is between 0-10
        return max(0.0, min(10.0, weighted_score))

    def _get_ideal_length_ratio(self, source_lang: str, target_lang: str) -> float:
        """
        Get ideal length ratio between source and target languages.

        Args:
            source_lang: Source language
            target_lang: Target language

        Returns:
            Ideal ratio of target/source text length
        """
        # Default 1:1 ratio
        default_ratio = 1.0

        # Known ratios for common language pairs (target/source)
        ratios = {
            ("Chinese", "English"): 1.5,  # Chinese to English expands
            ("English", "Chinese"): 0.6,  # English to Chinese contracts
            ("Japanese", "English"): 1.5,  # Japanese to English expands
            ("English", "Japanese"): 0.7,  # English to Japanese contracts
            ("Korean", "English"): 1.4,  # Korean to English expands
            ("English", "Korean"): 0.7,  # English to Korean contracts
            ("Spanish", "English"): 0.9,  # Spanish to English contracts slightly
            ("English", "Spanish"): 1.1,  # English to Spanish expands slightly
            ("German", "English"): 0.9,  # German to English contracts slightly
            ("English", "German"): 1.2,  # English to German expands
        }

        return ratios.get((source_lang, target_lang), default_ratio)

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
        # Calculate overall score from chunk scores (weighted by chunk length)
        if chunk_scores:
            overall_score = sum(chunk_scores) / len(chunk_scores)
        else:
            overall_score = 0.0

        # Final quality assessment
        final_assessment = {
            "overall": overall_score,
            "chunk_min": min(chunk_scores) if chunk_scores else 0.0,
            "chunk_max": max(chunk_scores) if chunk_scores else 0.0,
            "chunk_avg": overall_score,
            "sentences": len([s for s in full_target.split(".") if s.strip()]),
            "length_ratio": len(full_target) / len(full_source) if len(full_source) > 0 else 0.0,
        }

        return final_assessment

    def _get_quality_label(self, score: float) -> str:
        """
        Get a human-readable label for a quality score.

        Args:
            score: Quality score (0-10)

        Returns:
            Quality label
        """
        if score >= self.QUALITY_THRESHOLDS["excellent"]:
            return "Excellent"
        elif score >= self.QUALITY_THRESHOLDS["good"]:
            return "Good"
        elif score >= self.QUALITY_THRESHOLDS["acceptable"]:
            return "Acceptable"
        elif score >= self.QUALITY_THRESHOLDS["needs_review"]:
            return "Needs Review"
        else:
            return "Poor"

    def process_files(self) -> None:
        """Process all text files for translation or polishing with optimized parallelism"""
        # Find all files to process
        txt_files = self.find_text_files()
        total_files = len(txt_files)

        if total_files == 0:
            console.print("[yellow]No .txt files found in source directory.[/yellow]")
            return

        # Auto-detect source language if not specified
        if not self.config.source_language and self.config.auto_detect_language:
            detected_language = self.detect_files_language(txt_files)
            if detected_language:
                self.config.source_language = detected_language
                console.print(f"[green]Auto-detected source language: {detected_language}[/green]")
            else:
                console.print(
                    "[yellow]Could not automatically detect language. Please specify source language.[/yellow]"
                )
                return
        elif not self.config.source_language:
            console.print(
                "[yellow]Source language not specified and auto-detection disabled.[/yellow]"
            )
            return

        # Create job record if database is available
        job_id = None
        if self.db_manager:
            session = self.db_manager.create_session()
            job = TranslationJob(
                job_id=str(uuid.uuid4()),
                source_dir=str(self.config.source_dir),
                output_dir=str(self.config.output_dir),
                model_id=self.config.model,
                system_prompt=self.config.system_prompt,
                source_language=self.config.source_language,
                target_language=self.config.target_language,
                total_files=total_files,
                status="in_progress",
            )
            session.add(job)
            session.commit()
            job_id = job.job_id
            session.close()

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
        work_items = self._prepare_work_items(txt_files, job_id)

        # Estimate total chunks for progress tracking
        total_chunks = 0
        for item in work_items:
            try:
                # Read the file to get actual text
                text = Path(item["path"]).read_text(encoding="utf-8")

                # If file is small, it's just one chunk
                if len(text) <= self.config.max_chunk_size:
                    total_chunks += 1
                else:
                    # Otherwise, count actual chunks using the same splitter used during processing
                    chunks = self._split_text(text)
                    total_chunks += len(chunks)
            except Exception:
                # Fallback to estimation if we can't read the file
                total_chunks += max(1, (item["size"] // self.config.max_chunk_size))

        self.total_chunks_processed = 0
        self.start_time = time.time()
        self.processed_chunks_rate = []  # Store processing rates for estimation

        # Create file status dictionary to track per-file progress
        file_status = {str(item["path"]): {"chunks": 0, "total_chunks": 0} for item in work_items}

        # Set up enhanced progress tracking with time remaining
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}[/bold blue]"),
            BarColumn(bar_width=40),
            MofNCompleteColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            TextColumn("•"),
            TimeRemainingColumn(),
        )

        with progress:
            # Overall progress tracking
            file_task = progress.add_task(f"[cyan]Files", total=len(work_items))
            chunk_task = progress.add_task(f"[green]Chunks", total=total_chunks, completed=0)

            # Current file tracking
            current_file_task = progress.add_task(f"[yellow]Current: ", visible=False)
            eta_task = progress.add_task(f"[magenta]ETA", visible=False)

            # Add overall quality tracking
            quality_task = progress.add_task(f"[blue]Overall Quality", visible=False)

            # Status tracker for completion
            completion_task = progress.add_task("[bold]Status", visible=False)

            # Results storage
            results = {}
            quality_data = {}
            active_files = set()
            last_processed_file = None

            # Process files in parallel with optimized worker count
            with ThreadPoolExecutor(max_workers=worker_count) as executor:
                # Create partial function with fixed arguments
                process_func = partial(
                    self.process_file_optimized,
                    progress=progress,
                    file_task_id=file_task,
                    chunk_task_id=chunk_task,
                    current_file_task_id=current_file_task,
                    file_status=file_status,
                    active_files=active_files,
                    job_id=job_id,
                )

                # Submit all work items
                future_to_path = {
                    executor.submit(process_func, item): item["path"] for item in work_items
                }

                # Process results as they complete
                for future in as_completed(future_to_path):
                    path = future_to_path[future]
                    last_processed_file = path
                    active_files.discard(str(path))

                    # Update ETA based on current progress
                    if self.total_chunks_processed > 0:
                        elapsed = time.time() - self.start_time
                        rate = self.total_chunks_processed / elapsed
                        remaining_chunks = total_chunks - self.total_chunks_processed
                        eta_seconds = remaining_chunks / rate if rate > 0 else 0

                        eta = datetime.timedelta(seconds=int(eta_seconds))
                        progress.update(eta_task, description=f"[magenta]ETA: {eta}", visible=True)

                    result = future.result()
                    if result:
                        output_path, content, quality_metrics = result
                        results[str(output_path)] = content
                        quality_data[str(output_path)] = quality_metrics

                        # Update overall quality display
                        if quality_data:
                            avg_quality = sum(q["overall"] for q in quality_data.values()) / len(
                                quality_data
                            )
                            quality_label = self._get_quality_label(avg_quality)
                            progress.update(
                                quality_task,
                                description=f"[blue]Overall Quality: {avg_quality:.2f}/10 ({quality_label})",
                                visible=True,
                            )

        # Set final display state for progress bars
        # First show we're wrapping up
        progress.update(completion_task, description="[yellow]Finalizing results...", visible=True)

        # Show the last file as completed
        if last_processed_file:
            last_file_name = last_processed_file.name
            progress.update(
                current_file_task, description=f"[green]Completed: {last_file_name}", visible=True
            )

        # Update main progress bars to show completion
        progress.update(
            file_task, completed=len(work_items), description="[green]Files [Completed]"
        )
        progress.update(chunk_task, completed=total_chunks, description="[green]Chunks [Completed]")

        # Update quality and ETA for final display
        if quality_data:
            avg_quality = sum(q["overall"] for q in quality_data.values()) / len(quality_data)
            quality_label = self._get_quality_label(avg_quality)
            progress.update(
                quality_task,
                description=f"[green]Final Quality: {avg_quality:.2f}/10 ({quality_label})",
                completed=avg_quality,
                total=10,
                visible=True,
            )

        # Update ETA to show completed
        total_elapsed = time.time() - self.start_time
        elapsed_time = datetime.timedelta(seconds=int(total_elapsed))
        progress.update(eta_task, description=f"[green]Completed in: {elapsed_time}", visible=True)

        # Update completion status
        progress.update(
            completion_task, description="[green]Saving results to files...", visible=True
        )

        # Small delay to show the completed state
        time.sleep(0.5)

        # Write results to files after all processing is complete
        for output_path, content in results.items():
            path = Path(output_path).with_suffix(".txt")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

            # Create quality report file if quality scores are available
            if output_path in quality_data:
                quality_path = Path(output_path).with_suffix(".quality.json")
                try:
                    import json

                    with open(quality_path, "w") as f:
                        json.dump(quality_data[output_path], f, indent=2)
                except Exception as e:
                    logger.warning(f"Failed to save quality report: {e}")

        # Final completion status
        progress.update(
            completion_task,
            description="[bold green]✓ All tasks completed successfully!",
            visible=True,
        )

        # Small delay to show the final state before closing progress bars
        time.sleep(0.8)

        # Update job status if database is available
        if self.db_manager and job_id:
            session = self.db_manager.create_session()
            job = session.query(TranslationJob).filter_by(job_id=job_id).first()
            if job:
                job.status = "completed"
                job.end_time = datetime.datetime.utcnow()

            # Add overall quality score to job
            if quality_data:
                job.quality_score = sum(q["overall"] for q in quality_data.values()) / len(
                    quality_data
                )

            session.commit()
        session.close()

        # Display quality summary
        if quality_data:
            avg_quality = sum(q["overall"] for q in quality_data.values()) / len(quality_data)
            quality_label = self._get_quality_label(avg_quality)
            console.print(
                f"\n[bold blue]Overall Translation Quality: {avg_quality:.2f}/10 ({quality_label})[/bold blue]"
            )

        # Show files that might need review
        review_files = [
            (path, data["overall"])
            for path, data in quality_data.items()
            if data["overall"] < self.QUALITY_THRESHOLDS["acceptable"]
        ]

        if review_files:
            console.print("[yellow]Files that might need manual review:[/yellow]")
            for path, score in sorted(review_files, key=lambda x: x[1]):
                label = self._get_quality_label(score)
                console.print(f"  - {Path(path).name}: {score:.2f}/10 ({label})")

        # Calculate and display some statistics about the run
        total_elapsed = time.time() - self.start_time
        if total_chunks > 0 and total_elapsed > 0:
            chunks_per_second = total_chunks / total_elapsed
            console.print(f"[cyan]Processing speed: {chunks_per_second:.2f} chunks/second[/cyan]")

        if len(work_items) > 0 and total_elapsed > 0:
            files_per_minute = (len(work_items) / total_elapsed) * 60
            console.print(f"[cyan]Average throughput: {files_per_minute:.2f} files/minute[/cyan]")

    console.print("\n[bold green]✨ Translation completed successfully! ✨[/bold green]")

    # Keep existing helper methods unchanged
    def _create_file_record(self, job_id: str, source_path: str, output_path: str) -> None:
        """Create file record in database"""
        if not self.db_manager:
            return

        session = self.db_manager.create_session()
        file_record = TranslationFile(
            job_id=job_id, source_path=source_path, output_path=output_path, status="pending"
        )
        session.add(file_record)
        session.commit()
        session.close()

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
        if not self.db_manager:
            return

        session = self.db_manager.create_session()
        try:
            file_record = (
                session.query(TranslationFile)
                .filter_by(job_id=job_id, source_path=source_path)
                .first()
            )

            if file_record:
                file_record.status = status
                file_record.end_time = datetime.datetime.utcnow()
                if error:
                    file_record.error = error
                if quality_score is not None:
                    file_record.quality_score = quality_score

                # Update the job's completed_files counter if status is 'completed' or 'skipped'
                if status in ("completed", "skipped"):
                    job = session.query(TranslationJob).filter_by(job_id=job_id).first()
                    if job:
                        job.completed_files = job.completed_files + 1

                session.commit()
        finally:
            session.close()
