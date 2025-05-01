"""File handling operations for translation processing"""

import datetime
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from transphrase.core.config import TranslationConfig
from transphrase.database.models import DBManager, TranslationFile, TranslationJob

logger = logging.getLogger("translator")


class FileHandlers:
    """Handles file operations for translation processing"""

    def __init__(self, config: TranslationConfig, db_manager: Optional[DBManager] = None):
        """
        Initialize file handlers

        Args:
            config: Translation configuration
            db_manager: Database manager instance
        """
        self.config = config
        self.db_manager = db_manager

    def find_text_files(self) -> List[Dict[str, Any]]:
        """
        Find all supported text files in source directory, including HTML files

        Returns:
            List of dictionaries containing file information with keys:
            - path: Path object to the file
            - rel_path: Relative path from source directory
            - out_path: Output path in target directory
            - size: File size in bytes
        """
        # Define supported file extensions
        supported_extensions = [".txt", ".html"]

        # Log the source directory being searched
        logger.info(f"Searching for files in: {self.config.source_dir}")

        # Find all files with supported extensions
        files = []
        for ext in supported_extensions:
            found = sorted(self.config.source_dir.rglob(f"*{ext}"))
            logger.debug(f"Found {len(found)} {ext} files in {self.config.source_dir}")
            files.extend(found)

        # Log found files by type
        file_counts = {ext: 0 for ext in supported_extensions}
        for file in files:
            ext = file.suffix.lower()
            if ext in file_counts:
                file_counts[ext] += 1

        # Log the results
        for ext, count in file_counts.items():
            if count > 0:
                logger.info(f"Found {count} {ext} files")
            else:
                logger.debug(f"No {ext} files found")

        if not files:
            logger.warning(f"No supported files found ({', '.join(supported_extensions)})")
            return []

        # Prepare file information in the expected format
        file_info = []
        for file in files:
            rel = file.relative_to(self.config.source_dir)
            out_path = self.config.output_dir / rel.with_suffix(file.suffix)

            try:
                file_size = file.stat().st_size
            except OSError:
                file_size = 0

            file_info.append(
                {"path": file, "rel_path": rel, "out_path": out_path, "size": file_size}
            )

        return file_info

    def _prepare_work_items(self, files_to_process, job_id=None):
        """
        Prepare work items for processing

        Args:
            files_to_process: List of file information dictionaries
            job_id: Optional job ID for database

        Returns:
            List of work items with processing information
        """
        work_items = []

        for file_info in files_to_process:
            # Extract the path from the dictionary
            path = file_info["path"]  # This should be a Path object

            # Calculate relative path from source directory
            rel = path.relative_to(self.config.source_dir)

            # Create output path
            out_path = self.config.output_dir / rel

            # Add to work items
            work_item = {
                "path": path,
                "rel_path": rel,
                "out_path": out_path,
                "size": file_info.get("size", 0),
                "priority": file_info.get("priority", 0),
            }
            work_items.append(work_item)

            # Create database record if available
            if self.db_manager and job_id:
                # Convert Path objects to strings before passing to database
                self._create_file_record(job_id, str(path), str(rel))

        return work_items

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
