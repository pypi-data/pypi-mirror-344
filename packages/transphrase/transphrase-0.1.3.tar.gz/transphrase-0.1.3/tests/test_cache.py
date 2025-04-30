"""Tests for translation cache."""

import os
import tempfile
import time
from pathlib import Path

import pytest

from transphrase.cache.translation_cache import TranslationCache


@pytest.fixture
def temp_cache():
    """Create a temporary cache for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = TranslationCache(cache_dir=tmpdir, ttl=10)
        yield cache


def test_cache_init(temp_cache):
    """Test cache initialization."""
    assert temp_cache.ttl == 10
    assert temp_cache.cache_dir.exists()


def test_cache_set_get(temp_cache):
    """Test setting and getting cached translations."""
    # Set a value
    temp_cache.set("test text", "test prompt", "test-model", "translated text")

    # Get the value
    result = temp_cache.get("test text", "test prompt", "test-model")

    assert result == "translated text"


def test_cache_expiration(temp_cache):
    """Test cache entry expiration."""
    # Set the TTL to 1 second for this test
    temp_cache.ttl = 1

    # Set a value
    temp_cache.set("test text", "test prompt", "test-model", "translated text")

    # Verify it exists
    assert temp_cache.get("test text", "test prompt", "test-model") == "translated text"

    # Wait for it to expire
    time.sleep(2)

    # Verify it's gone
    assert temp_cache.get("test text", "test prompt", "test-model") is None


def test_cache_different_keys(temp_cache):
    """Test that different inputs produce different cache entries."""
    temp_cache.set("text1", "prompt", "model", "translation1")
    temp_cache.set("text2", "prompt", "model", "translation2")
    temp_cache.set("text1", "different prompt", "model", "translation3")
    temp_cache.set("text1", "prompt", "different model", "translation4")

    assert temp_cache.get("text1", "prompt", "model") == "translation1"
    assert temp_cache.get("text2", "prompt", "model") == "translation2"
    assert temp_cache.get("text1", "different prompt", "model") == "translation3"
    assert temp_cache.get("text1", "prompt", "different model") == "translation4"
