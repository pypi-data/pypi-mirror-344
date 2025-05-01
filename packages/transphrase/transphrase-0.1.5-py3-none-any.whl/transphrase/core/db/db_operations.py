"""Database operations for translation processing"""

import uuid
from typing import Optional

from transphrase.database.models import DBManager, TranslationFile, TranslationJob


class DatabaseOperations:
    """Handles database operations for translation processing"""

    def __init__(self, db_manager: Optional[DBManager] = None):
        """
        Initialize database operations

        Args:
            db_manager: Database manager instance
        """
        self.db_manager = db_manager

    def create_job_record(
        self,
        source_dir: str,
        output_dir: str,
        model: str,
        system_prompt: str,
        source_language: str,
        target_language: str,
        total_files: int,
    ) -> Optional[str]:
        """
        Create a new job record in the database

        Args:
            source_dir: Source directory path
            output_dir: Output directory path
            model: Model ID
            system_prompt: System prompt
            source_language: Source language
            target_language: Target language
            total_files: Total number of files

        Returns:
            Job ID if successful, None otherwise
        """
        if not self.db_manager:
            return None

        session = self.db_manager.create_session()
        job = TranslationJob(
            job_id=str(uuid.uuid4()),
            source_dir=source_dir,
            output_dir=output_dir,
            model_id=model,
            system_prompt=system_prompt,
            source_language=source_language,
            target_language=target_language,
            total_files=total_files,
            status="in_progress",
        )
        session.add(job)
        session.commit()
        job_id = job.job_id
        session.close()
        return job_id

    def update_job_status(self, job_id: str, status: str, quality_score: Optional[float] = None):
        """
        Update job status in database

        Args:
            job_id: Job ID
            status: New status
            quality_score: Optional quality score

        Note:
            If `self.db_manager` is not set, this method will log a warning and perform no operation.
        """
        if not self.db_manager:
            import logging

            logging.warning("Database manager is not set. Cannot update job status.")
            return

        session = self.db_manager.create_session()
        job = session.query(TranslationJob).filter_by(job_id=job_id).first()
        if job:
            job.status = status
            if quality_score is not None:
                job.quality_score = quality_score
            session.commit()
        session.close()

    def _update_file_status(
        self,
        job_id: str,
        file_path: str,
        status: str,
        error: Optional[str] = None,
        quality_score: Optional[float] = None,
    ):
        """
        Update the status of a translation file in the database

        Args:
            job_id: Job ID
            file_path: Path to the file
            status: New status (completed, failed, etc)
            error: Optional error message if failed
            quality_score: Optional quality score
        """
        if not self.db_manager:
            return

        session = self.db_manager.create_session()
        file_record = (
            session.query(TranslationFile).filter_by(job_id=job_id, source_path=file_path).first()
        )

        if file_record:
            file_record.status = status
            if error:
                file_record.error = error
            if quality_score is not None:
                file_record.quality_score = quality_score
            session.commit()
        session.close()
