"""Tests for API handler."""

from unittest.mock import MagicMock, patch

import pytest
from openai import RateLimitError

from transphrase.api.handler import APIHandler


@pytest.fixture
def api_handler():
    """Create a test API handler with mock components."""
    with patch("openai.OpenAI"):
        handler = APIHandler(api_key="test_key")
        handler.client = MagicMock()
        handler.cache = MagicMock()
        handler.rate_limiter = MagicMock()
        return handler


def test_api_handler_init():
    """Test API handler initialization."""
    with patch("openai.OpenAI") as mock_openai:
        handler = APIHandler(api_key="test_key", base_url="https://test.api")
        mock_openai.assert_called_once_with(api_key="test_key", base_url="https://test.api")
        assert handler.cache is None
        assert handler.rate_limiter is None


def test_translate_chunk_success(api_handler):
    """Test successful translation."""
    # Set up mock response
    mock_choice = MagicMock()
    mock_choice.message.content = "Translated text"
    api_handler.client.chat.completions.create.return_value.choices = [mock_choice]

    # Test translation
    result = api_handler.translate_chunk("Test prompt", "Test text", "test-model")

    # Verify calls
    api_handler.client.chat.completions.create.assert_called_once()
    api_handler.rate_limiter.before_request.assert_called_once()
    api_handler.rate_limiter.after_response.assert_called_once()
    api_handler.cache.get.assert_called_once()
    api_handler.cache.set.assert_called_once()

    assert result == "Translated text"


def test_translate_chunk_cache_hit(api_handler):
    """Test translation with cache hit."""
    api_handler.cache.get.return_value = "Cached translation"

    result = api_handler.translate_chunk("Test prompt", "Test text", "test-model")

    api_handler.client.chat.completions.create.assert_not_called()
    assert result == "Cached translation"


def test_translate_chunk_rate_limit_error(api_handler):
    """Test handling of rate limit errors."""
    error_response = RateLimitError(
        "Rate limit exceeded. Try again in 30 seconds.", response=MagicMock()
    )
    api_handler.client.chat.completions.create.side_effect = error_response

    # Test that the exception is propagated for retry
    with pytest.raises(RateLimitError):
        api_handler.translate_chunk("Test prompt", "Test text", "test-model")

    # Verify rate limiter was updated with error status
    api_handler.rate_limiter.after_response.assert_called_once()
    # The second parameter is headers, third is status_code which should be 429
    assert api_handler.rate_limiter.after_response.call_args[0][2] == 429


def test_fetch_available_models(api_handler):
    """Test fetching available models."""
    # Set up mock model data
    mock_model = MagicMock()
    mock_model.id = "test-model"
    mock_model.model_dump.return_value = {
        "id": "test-model",
        "description": "Test model description",
        "tokens": 4096,
        "pricing": {"input": 0.001, "output": 0.002},
        "metadata": {"vision": True},
    }
    api_handler.client.models.list.return_value.data = [mock_model]

    # Test model fetching
    models = api_handler.fetch_available_models()

    assert len(models) == 1
    assert models[0]["id"] == "test-model"
    assert models[0]["description"] == "Test model description"
    assert models[0]["tokens"] == 4096
    assert models[0]["pricing"] == "In: $0.001 | Out: $0.002"
    assert models[0]["capabilities"] == "Vision"
