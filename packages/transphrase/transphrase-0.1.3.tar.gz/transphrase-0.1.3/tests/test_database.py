"""Tests for database functionality."""

import datetime
import os  # Add this import
import tempfile
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from transphrase.database.models import (
    Base,
    DBManager,
    TranslationFile,
    TranslationJob,
    TranslationModel,
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        db_path = tmp.name
        engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

        yield engine, Session


def test_db_manager_init():
    """Test database manager initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        manager = DBManager(db_path)

        # Verify database file was created
        assert os.path.exists(db_path)

        # Verify session factory works
        session = manager.create_session()
        session.close()


def test_translation_model(temp_db):
    """Test TranslationModel operations."""
    _, Session = temp_db
    session = Session()

    # Create a model entry
    model = TranslationModel(
        model_id="test-model",
        description="Test model description",
        tokens=4096,
        pricing_input=0.001,
        pricing_output=0.002,
        capabilities="Vision, Chat",
        is_favorite=True,
        last_used=datetime.datetime.now(),
    )
    session.add(model)
    session.commit()

    # Retrieve and verify
    retrieved = session.query(TranslationModel).filter_by(model_id="test-model").first()
    assert retrieved is not None
    assert retrieved.description == "Test model description"
    assert retrieved.tokens == 4096
    assert retrieved.is_favorite is True

    session.close()


def test_translation_job(temp_db):
    """Test TranslationJob operations."""
    _, Session = temp_db
    session = Session()

    # Create a model first
    model = TranslationModel(model_id="test-model", description="Test model description")
    session.add(model)
    session.commit()

    # Create a job
    job = TranslationJob(
        job_id="test-job-123",
        source_dir="/tmp/source",
        output_dir="/tmp/output",
        model_id="test-model",
        system_prompt="Test prompt",
        source_language="Japanese",
        target_language="English",
        total_files=10,
        completed_files=0,
        status="in_progress",
    )
    session.add(job)
    session.commit()

    # Retrieve and verify
    retrieved = session.query(TranslationJob).filter_by(job_id="test-job-123").first()
    assert retrieved is not None
    assert retrieved.source_language == "Japanese"
    assert retrieved.target_language == "English"
    assert retrieved.status == "in_progress"
    assert retrieved.total_files == 10
    assert retrieved.completed_files == 0

    # Test relationships
    assert retrieved.model.model_id == "test-model"

    session.close()


def test_translation_file(temp_db):
    """Test TranslationFile operations."""
    _, Session = temp_db
    session = Session()

    # Create a job first
    job = TranslationJob(
        job_id="test-job-123",
        source_dir="/tmp/source",
        output_dir="/tmp/output",
        system_prompt="Test prompt",
        total_files=10,
        status="in_progress",
    )
    session.add(job)

    # Create file records
    file1 = TranslationFile(
        job_id="test-job-123",
        source_path="chapter1.txt",
        output_path="output/chapter1.txt",
        status="completed",
        start_time=datetime.datetime.now(),
        end_time=datetime.datetime.now(),
        tokens_input=1000,
        tokens_output=1200,
    )

    file2 = TranslationFile(
        job_id="test-job-123",
        source_path="chapter2.txt",
        output_path="output/chapter2.txt",
        status="failed",
        start_time=datetime.datetime.now(),
        error="API error",
    )

    session.add_all([file1, file2])
    session.commit()

    # Test relationship from job to files
    job = session.query(TranslationJob).filter_by(job_id="test-job-123").first()
    assert len(job.translations) == 2

    # Test querying files
    completed = session.query(TranslationFile).filter_by(status="completed").all()
    assert len(completed) == 1
    assert completed[0].source_path == "chapter1.txt"

    failed = session.query(TranslationFile).filter_by(status="failed").all()
    assert len(failed) == 1
    assert failed[0].error == "API error"

    session.close()
