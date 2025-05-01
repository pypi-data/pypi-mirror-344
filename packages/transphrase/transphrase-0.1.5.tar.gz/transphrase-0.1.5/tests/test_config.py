"""Tests for configuration module."""

from pathlib import Path

import pytest

from transphrase.core.config import (
    DEFAULT_MODEL,
    SUPPORTED_LANGUAGES,
    TRANSLATION_PROMPT_TEMPLATE,
    TranslationConfig,
)
from transphrase.rate_limiting.rate_limiter import RateLimitConfig


def test_translation_config_defaults():
    """Test default values in TranslationConfig."""
    config = TranslationConfig(
        api_key="test_key",
        model="test_model",
        system_prompt="test_prompt",
        workers=2,
        skip_existing=True,
        source_dir=Path("/tmp/source"),
        output_dir=Path("/tmp/output"),
    )

    assert config.api_key == "test_key"
    assert config.model == "test_model"
    assert config.source_language == "Chinese"
    assert config.target_language == "English"
    assert config.use_cache is True
    assert config.cache_ttl == 86400
    assert config.plugin_dirs == []
    assert isinstance(config.rate_limit_config, RateLimitConfig)
    assert config.db_path == "~/.transphrase/transphrase.db"


def test_translation_prompt_template():
    """Test prompt template formatting."""
    prompt = TRANSLATION_PROMPT_TEMPLATE.format(
        source_language="Japanese", target_language="German"
    )

    assert "Japanese text into high-quality German" in prompt
    assert "no Japanese characters" in prompt
    assert "German reads smoothly" in prompt


def test_supported_languages():
    """Test that required languages are supported."""
    required_languages = ["English", "Chinese", "Japanese", "Korean", "Spanish", "French", "German"]
    for lang in required_languages:
        assert lang in SUPPORTED_LANGUAGES
