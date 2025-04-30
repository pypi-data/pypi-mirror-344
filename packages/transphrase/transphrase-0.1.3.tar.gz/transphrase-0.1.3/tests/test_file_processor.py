"""Tests for file processor."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from transphrase.core.config import TranslationConfig
from transphrase.core.file_processor import FileProcessor


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

    config = TranslationConfig(
        api_key="test_key",
        model="test-model",
        system_prompt="test prompt",
        workers=1,
        skip_existing=False,
        source_dir=Path(source_dir),
        output_dir=Path(output_dir),
    )

    api_handler = MagicMock()
    api_handler.translate_chunk.return_value = "Translated content"

    db_manager = MagicMock()

    processor = FileProcessor(config, api_handler, db_manager)
    return processor


def test_find_text_files(mock_processor, setup_dirs):
    """Test finding text files."""
    files = mock_processor.find_text_files()
    assert len(files) == 1
    assert files[0].name == "test.txt"


def test_split_text(mock_processor):
    """Test text splitting functionality."""
    # Create a long text with multiple paragraphs
    long_text = "\n\n".join(["Paragraph " + str(i) * 1000 for i in range(5)])

    chunks = mock_processor._split_text(long_text)

    assert len(chunks) > 1  # Should be split into multiple chunks
    assert all(len(chunk) <= 4000 for chunk in chunks)  # Each chunk should be within limit


def test_translate_file(mock_processor, setup_dirs):
    """Test file translation."""
    source_dir, output_dir = setup_dirs
    source_path = Path(source_dir) / "test.txt"
    output_path = Path(output_dir) / "test.txt"

    # Create a mock progress tracker
    mock_progress = MagicMock()

    # Translate the file
    mock_processor.translate_file(source_path, output_path, mock_progress, "task1")

    # Verify translation occurred
    mock_processor.api_handler.translate_chunk.assert_called_once()

    # Verify output file was created
    assert output_path.exists()

    # Verify content
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert content == "Translated content"

    # Verify progress was updated
    mock_progress.update.assert_called_once()


@patch("transphrase.core.file_processor.ThreadPoolExecutor")
@patch("transphrase.core.file_processor.Progress")
def test_process_files(mock_progress_cls, mock_executor_cls, mock_processor):
    """Test file processing workflow."""
    # Setup mocks
    mock_progress = MagicMock()
    mock_progress_cls.return_value.__enter__.return_value = mock_progress

    mock_executor = MagicMock()
    mock_executor_cls.return_value.__enter__.return_value = mock_executor

    # Run the method
    mock_processor.process_files()

    # Verify executor was created with correct worker count
    mock_executor_cls.assert_called_once_with(max_workers=1)

    # Verify jobs were submitted
    assert mock_executor.submit.called

    # Verify progress was initialized
    assert mock_progress.add_task.called

    # Verify database was updated (job created and finalized)
    mock_processor.db_manager.create_session.assert_called()
