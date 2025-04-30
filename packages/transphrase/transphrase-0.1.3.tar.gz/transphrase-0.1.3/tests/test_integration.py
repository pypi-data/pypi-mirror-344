"""Integration tests for TransPhrase."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from transphrase.api.handler import APIHandler
from transphrase.cache.translation_cache import TranslationCache
from transphrase.core.config import TranslationConfig
from transphrase.core.file_processor import FileProcessor
from transphrase.database.models import DBManager, TranslationJob  # Add TranslationJob here
from transphrase.rate_limiting.rate_limiter import AdaptiveRateLimiter


@pytest.fixture
def setup_translation_env():
    """Set up a full translation environment."""
    with tempfile.TemporaryDirectory() as source_dir, tempfile.TemporaryDirectory() as output_dir, tempfile.TemporaryDirectory() as cache_dir, tempfile.NamedTemporaryFile(
        suffix=".db"
    ) as db_file:

        # Create test files
        source_path = Path(source_dir) / "chapter1.txt"
        with open(source_path, "w", encoding="utf-8") as f:
            f.write(
                "这是一个测试文本。我们将翻译它。"
            )  # "This is a test text. We will translate it." in Chinese

        # Create configuration
        config = TranslationConfig(
            api_key="test_key",
            model="test-model",
            system_prompt="Translate from Chinese to English",
            workers=1,
            skip_existing=False,
            source_dir=Path(source_dir),
            output_dir=Path(output_dir),
            source_language="Chinese",
            target_language="English",
            use_cache=True,
            cache_ttl=3600,
            db_path=db_file.name,
        )

        # Create components
        cache = TranslationCache(cache_dir=cache_dir)
        rate_limiter = AdaptiveRateLimiter()
        db_manager = DBManager(db_file.name)

        yield config, cache, rate_limiter, db_manager, source_dir, output_dir


@patch("openai.OpenAI")
def test_full_translation_flow(mock_openai, setup_translation_env):
    """Test full translation workflow from end to end."""
    config, cache, rate_limiter, db_manager, source_dir, output_dir = setup_translation_env

    # Mock OpenAI client
    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    # Set up response for model listing
    mock_model = MagicMock()
    mock_model.id = "test-model"
    mock_model.model_dump.return_value = {
        "id": "test-model",
        "description": "Test model",
    }
    mock_client.models.list.return_value.data = [mock_model]

    # Set up response for translation
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This is a test text. We will translate it."
    mock_client.chat.completions.create.return_value = mock_response

    # Create API handler
    api_handler = APIHandler(
        api_key=config.api_key,
        base_url="https://api.test.com",
        cache=cache,
        rate_limiter=rate_limiter,
    )

    # Create and run file processor
    processor = FileProcessor(config, api_handler, db_manager)
    processor.process_files()

    # Verify translation request was made
    mock_client.chat.completions.create.assert_called_once()

    # Verify translation was saved
    output_file = Path(output_dir) / "chapter1.txt"
    assert output_file.exists()

    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert content == "This is a test text. We will translate it."

    # Verify translation was cached
    cached_result = cache.get(
        "这是一个测试文本。我们将翻译它。", "Translate from Chinese to English", "test-model"
    )
    assert cached_result == "This is a test text. We will translate it."

    # Verify job was created in database
    session = db_manager.create_session()
    job = session.query(TranslationJob).first()
    assert job is not None
    assert job.model_id == "test-model"
    assert job.source_language == "Chinese"
    assert job.target_language == "English"
    assert job.status == "completed"
    assert job.total_files == 1
    assert job.completed_files == 1
    session.close()
