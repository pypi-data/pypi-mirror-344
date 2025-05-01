"""Tests for file processor."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from transphrase.core.config import TranslationConfig
from transphrase.core.processing.file_processor import FileProcessor


@pytest.fixture
def setup_dirs():
    """Set up temporary directories for testing."""
    with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as output_dir:
        # Create a test file
        source_path = Path(source_dir) / "test.txt"
        with open(source_path, "w", encoding="utf-8") as f:
            f.write("This is test content.")

        yield source_dir, output_dir


@pytest.fixture
def mock_processor(setup_dirs):
    """Create a mock file processor for testing."""
    source_dir, output_dir = setup_dirs

    # Add missing required attributes to config
    config = TranslationConfig(
        api_key="test_key",
        model="test-model",
        system_prompt="test prompt",
        workers=1,  # This is the correct parameter name
        skip_existing=False,
        source_dir=Path(source_dir),
        output_dir=Path(output_dir),
        source_language="English",
        target_language="Spanish",
        mode="translate",
        max_chunk_size=1000,
        auto_detect_language=False,
        use_context_cache=False,
        # Removed max_workers parameter
    )

    # Set max_workers as an attribute after initialization
    # This matches what _get_optimal_worker_count() expects
    config.max_workers = 1

    api_handler = MagicMock()
    api_handler.translate_chunk.return_value = "Translated content"

    db_manager = MagicMock()

    # Create processor with mocks
    processor = FileProcessor(config, api_handler, db_manager)

    # Set up database mocks more completely
    processor.db_operations = MagicMock()
    processor.db_operations.create_job_record.return_value = "test_job_id"
    processor.db_operations.update_job_status.return_value = None

    processor.db_manager = db_manager  # Initialize db_manager

    # Mock file handlers
    processor.file_handlers = MagicMock()
    processor.file_handlers.find_text_files.return_value = [
        {"path": Path(source_dir) / "test.txt", "size": 1000}
    ]
    processor.file_handlers._create_file_record.return_value = None
    processor.file_handlers._update_file_status.return_value = None
    processor.file_handlers._prepare_work_items.return_value = [
        {"path": Path(source_dir) / "test.txt", "size": 1000, "priority": 0}
    ]

    # Mock progress tracker
    processor.progress_tracker = MagicMock()
    processor.progress_tracker.total_chunks_processed = 0
    processor.progress_tracker.initialize.return_value = None
    processor.progress_tracker.finalize.return_value = None

    # Mock context tracker
    processor.context_tracker = MagicMock()
    processor.context_tracker.get_enhanced_prompt.return_value = "test prompt"
    processor.context_tracker.update_context.return_value = None

    # Mock chunk processor
    processor.chunk_processor = MagicMock()
    processor.chunk_processor.split_text.return_value = ["test chunk"]
    processor.chunk_processor.process_chunk.return_value = "Translated content"

    # Add these lines after the chunk_processor mock setup:
    processor._process_text_file = MagicMock()
    processor._process_text_file.return_value = (
        "Translated content",
        {"overall": 0.8, "fluency": 0.9, "consistency": 0.7},
    )
    processor._process_html_file = MagicMock()
    processor._process_html_file.return_value = (
        "Translated HTML content",
        {"overall": 0.8, "fluency": 0.9, "consistency": 0.7},
    )

    # Mock quality assessor methods
    processor.quality_assessor = MagicMock()
    processor.quality_assessor._assess_quality = MagicMock(return_value=0.85)
    processor.quality_assessor._calculate_quality_metrics = MagicMock(
        return_value={"overall": 0.8, "fluency": 0.9, "consistency": 0.7}
    )
    processor.quality_assessor.display_quality_summary = MagicMock()
    processor.quality_assessor.display_review_files = MagicMock()
    processor.quality_assessor.get_quality_label = MagicMock(return_value="Good")

    return processor


def test_find_processable_files(mock_processor, setup_dirs):
    """Test finding processable files."""
    files = mock_processor.find_processable_files()
    assert len(files) == 1
    assert files[0].name == "test.txt"


def test_split_text(mock_processor):
    """Test text splitting functionality."""
    # Create a long text with multiple paragraphs
    long_text = "\n\n".join(["Paragraph " + str(i) * 1000 for i in range(5)])

    chunks = mock_processor._split_text(long_text)

    # Verify we get at least one chunk
    assert len(chunks) >= 1
    # Verify chunks don't exceed max size
    assert all(len(chunk) <= mock_processor.config.max_chunk_size for chunk in chunks)


def test_process_single_file(mock_processor, setup_dirs):
    """Test processing a single file."""
    source_dir, output_dir = setup_dirs
    source_path = Path(source_dir) / "test.txt"
    output_path = Path(output_dir) / "test.txt"

    # Create the file if it doesn't exist
    if not source_path.exists():
        with open(source_path, "w", encoding="utf-8") as f:
            f.write("This is test content.")

    # Create mock progress and status tracking
    mock_progress = MagicMock()
    file_status = {str(source_path): {"chunks": 0, "total_chunks": 0}}
    active_files = set()

    # Configure mock to set up chunk splitting
    mock_processor.chunk_processor.split_text.return_value = ["This is test content."]

    # Process the file
    result = mock_processor._process_single_file(
        {"path": source_path},
        "test prompt",
        "test-model",
        mock_progress,
        "chunks_task",
        "file_task",
        file_status,
        active_files,
        "test_job_id",
    )

    # Verify file was processed
    assert result is not None

    # The rest of the test remains the same...


@patch("transphrase.core.processing.file_processor.ThreadPoolExecutor")
@patch("transphrase.core.processing.file_processor.Progress")
@patch("transphrase.core.processing.file_processor.as_completed")
def test_process_files(mock_as_completed, mock_progress_cls, mock_executor_cls, mock_processor):
    """Test file processing workflow."""
    # Setup mocks
    mock_progress = MagicMock()
    mock_progress_cls.return_value.__enter__.return_value = mock_progress

    # Mock executor and submitted future
    mock_future = MagicMock()
    mock_future.result.return_value = (Path("output.txt"), "Translated content", {"overall": 0.8})

    mock_executor = MagicMock()
    mock_executor.submit.return_value = mock_future
    mock_executor_cls.return_value.__enter__.return_value = mock_executor

    # Mock as_completed to return our mock futures
    mock_as_completed.return_value = [mock_future]

    # Remove the process_files_in_parallel mock to allow ThreadPoolExecutor to be called

    # Run the method with a timeout
    mock_processor.process_files()

    # Now this assertion should work
    mock_executor_cls.assert_called_once_with(max_workers=1)

    # Check db operations instead of direct db manager access
    mock_processor.db_operations.create_job_record.assert_called_once()

    # Verify progress was tracked
    assert mock_processor.progress_tracker.initialize.called
    assert mock_processor.progress_tracker.finalize.called
