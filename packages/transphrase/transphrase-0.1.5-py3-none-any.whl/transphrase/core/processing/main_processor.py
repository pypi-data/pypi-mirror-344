"""Main processing logic for translation"""

import datetime
import logging
import os
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console

from transphrase.api.handler import APIHandler
from transphrase.core.config import TranslationConfig
from transphrase.core.context_tracker import ContextTracker
from transphrase.core.db.db_operations import DatabaseOperations
from transphrase.core.quality.quality_assessor import QualityAssessor
from transphrase.core.utils.language_detector import LanguageDetector
from transphrase.database.models import DBManager, TranslationJob

from .file_handlers import FileHandlers
from .file_processor import FileProcessor
from .progress_tracker import ProgressTracker

logger = logging.getLogger("translator")
console = Console()


class MainProcessor:
    """Handles the main processing logic for translation"""

    def __init__(
        self,
        config: TranslationConfig,
        api_handler: APIHandler,
        db_manager: Optional[DBManager] = None,
    ):
        """
        Initialize main processor

        Args:
            config: Translation configuration
            api_handler: API handler for translation
            db_manager: Database manager instance
        """
        self.config = config
        self.api_handler = api_handler
        self.db_manager = db_manager

        # Initialize sub-processors
        self.language_detector = LanguageDetector()
        self.file_handlers = FileHandlers(config, db_manager)
        self.quality_assessor = QualityAssessor(config=config)
        self.db_operations = DatabaseOperations(db_manager)
        self.progress_tracker = ProgressTracker()

        # Create FileProcessor instance to handle file processing
        self.file_processor = FileProcessor(config, api_handler, db_manager)

        # Context tracking and threading locks
        self.context_tracker = None
        self.results_lock = threading.Lock()
        self.chunk_count_lock = threading.Lock()
        self.quality_scores = {}

    def _get_optimal_worker_count(self) -> int:
        """Determine optimal worker count based on system resources and rate limits"""
        # Delegate to FileProcessor's method
        return self.file_processor._get_optimal_worker_count()

    def process_files(self) -> None:
        """Process all text files for translation or polishing with optimized parallelism"""
        # Find all files to process
        files_to_process = self.file_handlers.find_text_files()
        total_files = len(files_to_process)

        if total_files == 0:
            console.print(
                "[yellow]No supported files found (.txt or .html) in source directory.[/yellow]"
            )
            return

        # Auto-detect source language if not specified
        if not self.config.source_language and self.config.auto_detect_language:
            # Include both txt and HTML files for language detection
            sample_files = [
                f["path"] for f in files_to_process if str(f["path"]).endswith((".txt", ".html"))
            ]

            if sample_files:
                logger.info(
                    f"Attempting to auto-detect language from {len(sample_files)} sample files"
                )

                # Show a progress message to the user
                console.print("[cyan]Analyzing file content to detect language...[/cyan]")

                # Perform language detection with enhanced script analysis
                detected_language = self.language_detector.detect_files_language(sample_files)

                if detected_language:
                    # Get a sample file for script analysis display
                    if sample_files:
                        try:
                            sample_text = Path(sample_files[0]).read_text(
                                encoding="utf-8", errors="ignore"
                            )[:1000]
                            script_info = self.language_detector._detect_script_type(sample_text)

                            # Format script info for display
                            if script_info:
                                dominant_script, percentage = max(
                                    script_info.items(), key=lambda x: x[1]
                                )
                                script_msg = (
                                    f" (dominant script: {dominant_script}, {percentage:.1%})"
                                )
                            else:
                                script_msg = ""

                            console.print(
                                f"[green]Auto-detected source language: {detected_language}{script_msg}[/green]"
                            )
                        except Exception as e:
                            # Fallback to simple message if script analysis fails
                            console.print(
                                f"[green]Auto-detected source language: {detected_language}[/green]"
                            )
                            logger.debug(f"Error during script analysis display: {e}")
                    else:
                        console.print(
                            f"[green]Auto-detected source language: {detected_language}[/green]"
                        )

                    self.config.source_language = detected_language
                else:
                    console.print(
                        "[yellow]Could not automatically detect language. Please specify source language.[/yellow]"
                    )
                    return
            else:
                console.print(
                    "[yellow]No suitable files found for language detection. Please specify source language.[/yellow]"
                )
                return
        elif not self.config.source_language:
            console.print(
                "[yellow]Source language not specified and auto-detection disabled.[/yellow]"
            )
            return

        # Create job record if database is available
        job_id = self.db_operations.create_job_record(
            source_dir=str(self.config.source_dir),
            output_dir=str(self.config.output_dir),
            model=self.config.model,
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

            # Share context tracker with the file processor
            self.file_processor.context_tracker = self.context_tracker

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
        work_items = self.file_handlers._prepare_work_items(files_to_process, job_id)

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
                    chunks = self.file_processor._split_text(text)
                    total_chunks += len(chunks)
            except Exception:
                # Fallback to estimation if we can't read the file
                total_chunks += max(1, (item["size"] // self.config.max_chunk_size))

        # Initialize progress tracking
        self.progress_tracker.total_chunks_processed = 0
        self.progress_tracker.start_time = time.time()

        # Create file status dictionary to track per-file progress
        file_status = {str(item["path"]): {"chunks": 0, "total_chunks": 0} for item in work_items}

        # Set up progress tracking with the ProgressTracker
        progress = self.progress_tracker.setup_progress(len(work_items), total_chunks)

        with progress:
            # Get task IDs from the progress tracker
            file_task = self.progress_tracker.file_task
            chunk_task = self.progress_tracker.chunk_task
            current_file_task = self.progress_tracker.current_file_task
            quality_task = self.progress_tracker.quality_task
            completion_task = self.progress_tracker.completion_task
            eta_task = self.progress_tracker.eta_task

            # Process files using FileProcessor's method for parallel processing
            results = self.file_processor.process_files_in_parallel(
                work_items,
                self.config.system_prompt,
                self.config.model,
                progress,
                job_id=job_id,
                files_task_id=self.progress_tracker.file_task,
                chunks_task_id=self.progress_tracker.chunk_task,
                current_file_task_id=self.progress_tracker.current_file_task,
            )

            # Extract results
            processed_files = []
            quality_data = {}

            for result in results:
                if result:
                    output_path, content, quality_metrics = result
                    if output_path and content and quality_metrics:
                        processed_files.append(output_path)
                        quality_data[str(output_path)] = quality_metrics

            # Update quality for final display
            if quality_data:
                avg_quality = sum(q["overall"] for q in quality_data.values()) / len(quality_data)
                quality_label = self.quality_assessor._get_quality_label(avg_quality)
                progress.update(
                    quality_task,
                    description=f"[green]Final Quality: {avg_quality:.2f}/10 ({quality_label})",
                    completed=avg_quality,
                    total=10,
                    visible=True,
                )

            # Update ETA to show completed
            total_elapsed = time.time() - self.progress_tracker.start_time
            elapsed_time = datetime.timedelta(seconds=int(total_elapsed))
            progress.update(
                eta_task, description=f"[green]Completed in: {elapsed_time}", visible=True
            )

            # Update completion status
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
            quality_label = self.quality_assessor._get_quality_label(avg_quality)
            console.print(
                f"\n[bold blue]Overall Translation Quality: {avg_quality:.2f}/10 ({quality_label})[/bold blue]"
            )

        # Show files that might need review
        review_files = [
            (path, data["overall"])
            for path, data in quality_data.items()
            if data["overall"] < self.quality_assessor.QUALITY_THRESHOLDS["acceptable"]
        ]

        if review_files:
            console.print("[yellow]Files that might need manual review:[/yellow]")
            for path, score in sorted(review_files, key=lambda x: x[1]):
                label = self.quality_assessor._get_quality_label(score)
                console.print(f"  - {Path(path).name}: {score:.2f}/10 ({label})")

        # Calculate and display some statistics about the run
        total_elapsed = time.time() - self.progress_tracker.start_time
        if total_chunks > 0 and total_elapsed > 0:
            chunks_per_second = total_chunks / total_elapsed
            console.print(f"[cyan]Processing speed: {chunks_per_second:.2f} chunks/second[/cyan]")

        if len(work_items) > 0 and total_elapsed > 0:
            files_per_minute = (len(work_items) / total_elapsed) * 60
            console.print(f"[cyan]Average throughput: {files_per_minute:.2f} files/minute[/cyan]")
