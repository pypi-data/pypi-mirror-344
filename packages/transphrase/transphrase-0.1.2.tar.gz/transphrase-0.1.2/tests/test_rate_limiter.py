"""Tests for rate limiting module."""

import time
from unittest.mock import MagicMock, patch

import pytest

from transphrase.rate_limiting.rate_limiter import (
    AdaptiveRateLimiter,
    ModelRateLimit,
    RateLimitConfig,
    RateLimitExceededError,
    TokenBucket,
)


def test_rate_limit_config():
    """Test rate limit configuration."""
    config = RateLimitConfig(requests_per_minute=30, tokens_per_minute=60000)

    assert config.requests_per_minute == 30
    assert config.tokens_per_minute == 60000
    assert config.max_retries == 5
    assert config.initial_backoff == 1.0
    assert config.max_backoff == 60.0
    assert config.model_limits == {}

    # Test model-specific limits
    config.add_model_limit("test-model", 20, 40000)
    assert "test-model" in config.model_limits
    assert config.model_limits["test-model"].requests_per_minute == 20
    assert config.model_limits["test-model"].tokens_per_minute == 40000

    # Test get_model_limit
    req_limit, token_limit = config.get_model_limit("test-model")
    assert req_limit == 20
    assert token_limit == 40000

    # Test default limits for unknown model
    req_limit, token_limit = config.get_model_limit("unknown-model")
    assert req_limit == 30
    assert token_limit == 60000


def test_token_bucket():
    """Test token bucket rate limiter."""
    # Initialize with 10 tokens, refilling at 1 token per second
    bucket = TokenBucket(10, 1.0)

    # Initial state
    assert bucket.capacity == 10
    assert bucket.tokens == 10
    assert bucket.fill_rate == 1.0

    # Consume 5 tokens
    success, wait_time = bucket.consume(5)
    assert success is True
    assert wait_time == 0.0
    assert bucket.tokens == 5

    # Consume 6 tokens (more than available)
    success, wait_time = bucket.consume(6)
    assert success is False
    assert wait_time > 0  # Should need to wait for refill
    assert bucket.tokens == 5  # Tokens unchanged

    # Update capacity
    bucket.update_capacity(20, 2.0)
    assert bucket.capacity == 20
    assert bucket.fill_rate == 2.0
    assert bucket.tokens == 5  # Existing tokens preserved

    # Test metrics
    metrics = bucket.get_metrics()
    assert metrics["capacity"] == 20
    assert metrics["current_tokens"] == 5
    assert metrics["fill_rate"] == 2.0
    assert metrics["total_consumed"] == 5


def test_adaptive_rate_limiter():
    """Test adaptive rate limiter."""
    limiter = AdaptiveRateLimiter()

    # Test default config
    assert limiter.config.requests_per_minute == 20  # Modified from default 60
    assert limiter.config.tokens_per_minute == 128000  # Modified from default

    # Test before_request with no previous errors
    wait_time = limiter.before_request("test-model", 100)
    assert wait_time == 0  # Should not be limited initially

    # Test creating local limiter
    assert "test-model" in limiter.local_limiters
    local_limiter = limiter.local_limiters["test-model"]
    assert isinstance(local_limiter, TokenBucket)

    # Test after_response for successful request
    limiter.after_response("test-model", {}, 200)
    assert limiter.retry_counts.get("test-model", 0) == 0
    assert limiter.consecutive_successful_calls == 1

    # Test after_response for rate limit error
    limiter.after_response("test-model", {}, 429)
    assert limiter.retry_counts.get("test-model", 0) == 1
    assert limiter.consecutive_successful_calls == 0
    assert limiter.actual_rate_limits_detected is True

    # Test backoff calculation
    backoff = limiter._calculate_backoff("test-model")
    assert backoff > 0  # Should have some backoff after a rate limit error

    # Test global rate limit
    limiter.set_global_rate_limit(10)
    assert limiter.global_rate_limited is True
    assert limiter.global_rate_limit_until > time.time()

    # Test before_request with global rate limit
    wait_time = limiter.before_request("other-model", 10)
    assert wait_time > 0  # Should be rate limited due to global limit
