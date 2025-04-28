"""File processing operations for translation"""

import datetime
import logging
import os
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskID, TextColumn, TimeElapsedColumn

from transphrase.api.handler import APIHandler
from transphrase.core.config import MAX_CHUNK_SIZE, TranslationConfig
from transphrase.database.models import DBManager, TranslationFile, TranslationJob

logger = logging.getLogger("translator")
console = Console()


class FileProcessor:
    """Handles file processing operations for translation"""

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

    def find_text_files(self) -> List[Path]:
        """
        Find all text files in source directory

        Returns:
            List of paths to text files
        """
        return sorted(self.config.source_dir.rglob("*.txt"))

    def translate_file(
        self,
        input_path: Path,
        output_path: Path,
        progress: Progress,
        task_id: TaskID,
        job_id: Optional[str] = None,
    ) -> None:
        """
        Translate a single file

        Args:
            input_path: Path to input file
            output_path: Path to output file
            progress: Progress bar instance
            task_id: Task ID in progress bar
            job_id: Optional job ID for database update
        """
        try:
            # Read the text file
            text = input_path.read_text(encoding="utf-8")

            # Split into chunks if needed
            if len(text) > MAX_CHUNK_SIZE:
                # Basic chunking by paragraphs - could be improved
                chunks = self._split_text(text)
                translated_chunks = []

                for chunk in chunks:
                    translated_chunk = self.api_handler.translate_chunk(
                        self.config.system_prompt, chunk, self.config.model
                    )
                    translated_chunks.append(translated_chunk)

                translation = "\n".join(translated_chunks)
            else:
                translation = self.api_handler.translate_chunk(
                    self.config.system_prompt, text, self.config.model
                )

            # Ensure output directory exists
            output_path = output_path.with_suffix(".txt")
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write translation to file
            output_path.write_text(translation, encoding="utf-8")

            # Log success
            logger.info(
                f"✅ Translated: {os.path.relpath(input_path, Path.cwd())} -> "
                f"{os.path.relpath(output_path, Path.cwd())}"
            )

            # Update database if available - mark as completed
            if self.db_manager and job_id:
                rel_path = input_path.relative_to(self.config.source_dir)
                self._update_file_status(job_id, str(rel_path), "completed")

        except Exception as e:
            # Log error
            logger.error(f"❌ Failed: {os.path.relpath(input_path, Path.cwd())} - {e}")

            # Update database with error if available
            if self.db_manager and job_id:
                rel_path = input_path.relative_to(self.config.source_dir)
                self._update_file_status(job_id, str(rel_path), "failed", str(e))

        finally:
            # Update progress
            progress.update(task_id, advance=1)

    def _split_text(self, text: str) -> List[str]:
        """
        Split text into manageable chunks for translation

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        # Split by paragraphs first
        paragraphs = text.split("\n\n")
        chunks: List[str] = []
        current_chunk = ""

        for para in paragraphs:
            # If adding this paragraph would exceed chunk size, start a new chunk
            if len(current_chunk) + len(para) + 2 > MAX_CHUNK_SIZE:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = para
            else:
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para

        # Add the last chunk if not empty
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def process_files(self) -> None:
        """Process all text files for translation"""
        txt_files = self.find_text_files()
        total = len(txt_files)

        if total == 0:
            console.print("[yellow]No .txt files found in source directory.[/yellow]")
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
                source_language=self.config.source_language,  # Add this
                target_language=self.config.target_language,  # Add this
                total_files=total,
                status="in_progress",
            )
            session.add(job)
            session.commit()
            job_id = job.job_id
            session.close()

        # Otherwise use local processing
        console.print(
            f"[bold green]Processing {total} files with {self.config.workers} workers\n"
            f"Translating: {self.config.source_language} → {self.config.target_language}\n"
            f"Using model: {self.config.model}[/bold green]"
        )

        progress = Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
        )

        with progress:
            task = progress.add_task("Processing", total=total)

            # Dynamic worker count based on rate limits
            worker_count = self.config.workers

            # Reduce worker count if rate limits have been hit recently
            if hasattr(self.api_handler, "rate_limiter") and self.api_handler.rate_limiter:
                if self.api_handler.rate_limiter.actual_rate_limits_detected:
                    worker_count = min(2, worker_count)  # Max 2 workers when rate limited
                    logger.info(f"Rate limits detected, reducing worker count to {worker_count}")

            with ThreadPoolExecutor(max_workers=worker_count) as executor:
                futures = []

                for path in txt_files:
                    rel = path.relative_to(self.config.source_dir)
                    out_path = self.config.output_dir / rel

                    # Skip existing files if configured
                    if self.config.skip_existing and out_path.with_suffix(".txt").exists():
                        logger.info(f"🔶 Skipping existing: {rel}")
                        progress.update(task, advance=1)

                        # Update database if available
                        if self.db_manager and job_id:
                            self._update_file_status(job_id, str(rel), "skipped")

                        continue

                    # Create file record in database if available
                    if self.db_manager and job_id:
                        self._create_file_record(job_id, str(rel), str(out_path))

                    # Submit translation task
                    futures.append(
                        executor.submit(self.translate_file, path, out_path, progress, task, job_id)
                    )

                # Wait for all tasks to complete
                for _ in as_completed(futures):
                    pass

        # Update job status if database is available
        if self.db_manager and job_id:
            session = self.db_manager.create_session()
            job = session.query(TranslationJob).filter_by(job_id=job_id).first()
            if job:
                job.status = "completed"
                job.end_time = datetime.datetime.utcnow()
                session.commit()
            session.close()

        console.print("\n[bold blue]All tasks completed![/bold blue]")

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
        self, job_id: str, source_path: str, status: str, error: str = None
    ) -> None:
        """Update file status in database and increment completed files counter"""
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

                # Update the job's completed_files counter if status is 'completed' or 'skipped'
                if status in ("completed", "skipped"):
                    job = session.query(TranslationJob).filter_by(job_id=job_id).first()
                    if job:
                        job.completed_files = job.completed_files + 1

                session.commit()
        finally:
            session.close()
