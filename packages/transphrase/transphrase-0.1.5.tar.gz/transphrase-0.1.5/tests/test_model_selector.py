"""Tests for model selector UI."""

from unittest.mock import MagicMock, patch

import pytest

from transphrase.api.handler import APIHandler
from transphrase.ui.model_selector import ModelSelector


@pytest.fixture
def mock_selector():
    """Create a mock model selector for testing."""
    mock_api = MagicMock(spec=APIHandler)

    # Set up mock models
    mock_models = [
        {
            "id": "model-1",
            "description": "First test model",
            "tokens": 4096,
            "pricing": "Free",
            "capabilities": "Basic",
        },
        {
            "id": "model-2",
            "description": "Second test model with advanced features",
            "tokens": 8192,
            "pricing": "Paid",
            "capabilities": "Advanced",
        },
        {
            "id": "gpt-3",
            "description": "OpenAI model",
            "tokens": 4000,
            "pricing": "Paid",
            "capabilities": "Chat",
        },
    ]

    mock_api.fetch_available_models.return_value = mock_models

    selector = ModelSelector(mock_api, default_model="model-2")
    # Pre-load models to avoid API call during tests
    selector.models_info = mock_models
    selector.models = [m["id"] for m in mock_models]

    return selector


def test_load_models(mock_selector):
    """Test loading models."""
    # Since we pre-loaded in the fixture, reload
    mock_selector.models_info = []
    mock_selector.models = []

    result = mock_selector._load_models()

    assert result is True
    assert len(mock_selector.models) == 3
    assert mock_selector.models == ["model-1", "model-2", "gpt-3"]
    assert mock_selector.api_handler.fetch_available_models.called


def test_filter_models(mock_selector):
    """Test model filtering."""
    # Test empty search (returns all)
    filtered = mock_selector._filter_models("")
    assert len(filtered) == 3

    # Test specific model search
    filtered = mock_selector._filter_models("gpt")
    assert len(filtered) == 1
    assert mock_selector.models_info[filtered[0]]["id"] == "gpt-3"

    # Test description search
    filtered = mock_selector._filter_models("advanced")
    assert len(filtered) == 1
    assert mock_selector.models_info[filtered[0]]["id"] == "model-2"

    # Test capability search
    filtered = mock_selector._filter_models("basic")
    assert len(filtered) == 1
    assert mock_selector.models_info[filtered[0]]["id"] == "model-1"

    # Test multi-match search
    filtered = mock_selector._filter_models("model")
    assert len(filtered) == 2
    assert set([mock_selector.models_info[i]["id"] for i in filtered]) == {"model-1", "model-2"}


@patch("transphrase.ui.model_selector.readchar.readkey")
@patch("transphrase.ui.model_selector.console.print")
def test_select_model_enter(mock_print, mock_readkey, mock_selector):
    """Test model selection with Enter key."""
    # Mock key presses: first down arrow, then Enter
    mock_readkey.side_effect = ["j", "\r"]

    selected = mock_selector.select_model()

    # Should select the model at index 1 after pressing down once
    assert selected == "model-2"


@patch("transphrase.ui.model_selector.readchar.readkey")
@patch("transphrase.ui.model_selector.console.print")
def test_select_model_esc(mock_print, mock_readkey, mock_selector):
    """Test model selection with Escape key."""
    # Press Escape key to select default
    mock_readkey.return_value = "\x1b"

    selected = mock_selector.select_model()

    # Should return the default model
    assert selected == "model-2"


@patch("transphrase.ui.model_selector.readchar.readkey")
@patch("transphrase.ui.model_selector.console.print")
def test_select_model_search_filter(mock_print, mock_readkey, mock_selector):
    """Test model filtering with search and then selection."""
    # Type "gpt", press enter
    mock_readkey.side_effect = ["g", "p", "t", "\r"]

    selected = mock_selector.select_model()

    # Should select the only model matching "gpt"
    assert selected == "gpt-3"
