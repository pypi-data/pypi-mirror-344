import logging
import math
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple

# Make Redis optional
try:
    import redis
    from redis.client import Redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# Configure logging
logger = logging.getLogger("rate_limiter")


@dataclass
class ModelRateLimit:
    """Rate limit settings for a specific model"""

    requests_per_minute: int
    tokens_per_minute: int


@dataclass
class RateLimitConfig:
    """Rate limit configuration"""

    requests_per_minute: int = 60
    tokens_per_minute: int = 120000  # Typical token limit for some APIs
    max_retries: int = 5
    initial_backoff: float = 1.0
    max_backoff: float = 60.0
    # Store model-specific limits
    model_limits: Dict[str, ModelRateLimit] = field(default_factory=dict)

    def get_model_limit(self, model: str) -> Tuple[int, int]:
        """Get rate limits for a specific model"""
        if model in self.model_limits:
            limit = self.model_limits[model]
            return limit.requests_per_minute, limit.tokens_per_minute
        return self.requests_per_minute, self.tokens_per_minute

    def add_model_limit(self, model: str, requests_per_minute: int, tokens_per_minute: int) -> None:
        """Add or update a model-specific rate limit"""
        self.model_limits[model] = ModelRateLimit(
            requests_per_minute=requests_per_minute, tokens_per_minute=tokens_per_minute
        )


class RateLimitExceededError(Exception):
    """Exception raised when rate limit is exceeded"""

    def __init__(self, wait_time: float, message: str = "Rate limit exceeded"):
        self.wait_time = wait_time
        self.message = f"{message}, retry after {wait_time:.2f} seconds"
        super().__init__(self.message)


class TokenBucket:
    """Token bucket rate limiter for local use"""

    def __init__(self, capacity: int, fill_rate: float):
        """
        Initialize token bucket

        Args:
            capacity: Maximum number of tokens in the bucket
            fill_rate: Tokens per second to add to the bucket
        """
        self.capacity = capacity
        self.fill_rate = fill_rate
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = threading.RLock()
        # Add metrics tracking
        self.total_consumed = 0
        self.total_limited = 0
        self.total_wait_time = 0.0

    def _refill(self) -> None:
        """Refill the token bucket based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_update
        new_tokens = elapsed * self.fill_rate

        with self.lock:
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_update = now

    def consume(self, tokens: int = 1, raise_on_limit: bool = False) -> Tuple[bool, float]:
        """
        Try to consume tokens from the bucket

        Args:
            tokens: Number of tokens to consume
            raise_on_limit: Whether to raise an exception if rate limited

        Returns:
            Tuple of (success, wait_time)
        Raises:
            RateLimitExceededError: If rate limited and raise_on_limit is True
        """
        self._refill()

        with self.lock:
            if tokens <= self.tokens:
                self.tokens -= tokens
                self.total_consumed += tokens
                return True, 0.0
            else:
                # Calculate wait time until enough tokens are available
                wait_time = (tokens - self.tokens) / self.fill_rate

                # Update metrics
                self.total_limited += 1
                self.total_wait_time += wait_time

                if raise_on_limit:
                    raise RateLimitExceededError(wait_time)
                return False, wait_time

    def get_metrics(self) -> Dict[str, Any]:
        """Get metrics about bucket usage"""
        with self.lock:
            return {
                "capacity": self.capacity,
                "current_tokens": self.tokens,
                "fill_rate": self.fill_rate,
                "total_consumed": self.total_consumed,
                "total_limited": self.total_limited,
                "total_wait_time": self.total_wait_time,
                "average_wait_time": (
                    self.total_wait_time / self.total_limited if self.total_limited > 0 else 0.0
                ),
            }

    def update_capacity(self, new_capacity: int, new_fill_rate: Optional[float] = None) -> None:
        """Update the bucket capacity and optionally the fill rate"""
        with self.lock:
            self._refill()  # Refill before changing capacity to avoid losing tokens
            tokens_ratio = self.tokens / self.capacity if self.capacity > 0 else 1.0
            self.capacity = new_capacity
            self.tokens = min(self.tokens, new_capacity)

            # Optionally update fill rate
            if new_fill_rate is not None:
                self.fill_rate = new_fill_rate


class DistributedRateLimiter:
    """Distributed rate limiter using Redis"""

    def __init__(
        self,
        redis_client: "Redis",
        key_prefix: str = "transphrase:rate_limit:",
        config: RateLimitConfig = None,
    ):
        """
        Initialize distributed rate limiter

        Args:
            redis_client: Redis client instance
            key_prefix: Prefix for Redis keys
            config: Rate limit configuration
        """
        self.redis = redis_client
        self.key_prefix = key_prefix
        self.config = config or RateLimitConfig()

        # Load Lua script for atomic rate limiting
        self.limit_script = self.redis.register_script(
            """
            local request_key = KEYS[1]
            local token_key = KEYS[2]
            local request_limit = tonumber(ARGV[1])
            local token_limit = tonumber(ARGV[2])
            local token_count = tonumber(ARGV[3])
            local expire_time = tonumber(ARGV[4])

            -- Get current values
            local current_requests = tonumber(redis.call('get', request_key) or "0")
            local current_tokens = tonumber(redis.call('get', token_key) or "0")

            -- Check if limits would be exceeded
            if current_requests >= request_limit or (current_tokens + token_count) > token_limit then
                return {0, current_requests, current_tokens}
            end

            -- Increment counters
            redis.call('incr', request_key)
            redis.call('incrby', token_key, token_count)

            -- Set expiration
            redis.call('expire', request_key, expire_time)
            redis.call('expire', token_key, expire_time)

            return {1, current_requests + 1, current_tokens + token_count}
        """
        )

        # Metrics
        self.total_consumed = 0
        self.total_limited = 0
        self.lock = threading.RLock()

    def consume(
        self, model: str, tokens: int = 1, raise_on_limit: bool = False
    ) -> Tuple[bool, float]:
        """
        Try to consume tokens from the distributed rate limiter

        Args:
            model: Model ID to rate limit
            tokens: Number of tokens to consume
            raise_on_limit: Whether to raise an exception if rate limited

        Returns:
            Tuple of (success, wait_time)
        Raises:
            RateLimitExceededError: If rate limited and raise_on_limit is True
        """
        request_key = f"{self.key_prefix}{model}:requests"
        token_key = f"{self.key_prefix}{model}:tokens"

        # Get model-specific limits
        request_limit, token_limit = self.config.get_model_limit(model)

        try:
            # Use Lua script for atomic operation
            result = self.limit_script(
                keys=[request_key, token_key], args=[request_limit, token_limit, tokens, 60]
            )

            success = bool(result[0])

            with self.lock:
                if success:
                    self.total_consumed += tokens
                    return True, 0.0
                else:
                    self.total_limited += 1
                    wait_time = 60.0  # Default wait time for simplicity

                    if raise_on_limit:
                        raise RateLimitExceededError(wait_time)
                    return False, wait_time
        except Exception as e:
            if not isinstance(e, RateLimitExceededError):
                logger.warning(f"Redis error in rate limiter: {e}")
            # On Redis errors, fall back to allowing the request
            # This is safer than blocking legitimate requests due to Redis issues
            return True, 0.0

    def get_metrics(self) -> Dict[str, Any]:
        """Get metrics about distributed rate limiter usage"""
        with self.lock:
            return {"total_consumed": self.total_consumed, "total_limited": self.total_limited}


class AdaptiveRateLimiter:
    """Adaptive rate limiter that adjusts based on API responses"""

    def __init__(self, redis_url: Optional[str] = None, config: RateLimitConfig = None):
        """
        Initialize adaptive rate limiter

        Args:
            redis_url: Redis URL for distributed rate limiting
            config: Rate limit configuration
        """
        self.config = config or RateLimitConfig()
        # Increase default limits if not specified
        if not self.config.model_limits:
            # Use a more generous default - 180 requests/min instead of 60
            self.config.requests_per_minute = 20
            self.config.tokens_per_minute = 128000  # Also increase token limit

        self.local_limiters: Dict[str, TokenBucket] = {}

        # Add a way to temporarily disable local rate limiting
        self.local_limiting_enabled = True

        # Initialize Redis client if URL is provided and Redis is available
        self.redis = None
        self.distributed_limiter = None

        # Track API responses to detect actual rate limits
        self.actual_rate_limits_detected = False
        self.consecutive_successful_calls = 0

        # For backoff strategy
        self.retry_counts: Dict[str, int] = {}

        # For tracking API health
        self.error_rates: Dict[str, float] = {}
        self.response_times: Dict[str, float] = {}

        # Metrics
        self.total_requests = 0
        self.total_limited = 0
        self.total_wait_time = 0.0

        # Add global rate limit flag and timer
        self.global_rate_limited = False
        self.global_rate_limit_until = 0.0
        self.global_rate_limit_lock = threading.Lock()

    def _get_local_limiter(self, model: str) -> TokenBucket:
        """Get or create local token bucket for the model"""
        if model not in self.local_limiters:
            # Get model-specific limits
            request_limit, token_limit = self.config.get_model_limit(model)

            # Create bucket with appropriate capacity - start with a full bucket
            # but use a more generous capacity than the default
            self.local_limiters[model] = TokenBucket(
                max(180, request_limit),  # Use at least 180 requests/min
                max(3.0, request_limit / 60.0),  # At least 3 tokens per second
            )
        return self.local_limiters[model]

    def _calculate_backoff(self, model: str) -> float:
        """Calculate exponential backoff time based on retry count"""
        retry_count = self.retry_counts.get(model, 0)
        if retry_count == 0:
            return 0.0

        backoff = min(
            self.config.max_backoff, self.config.initial_backoff * (2 ** (retry_count - 1))
        )

        # Add jitter to avoid thundering herd problem
        jitter = backoff * 0.1 * (2 * (0.5 - abs(time.time() % 1 - 0.5)))
        return backoff + jitter

    def before_request(self, model: str, tokens: int = 1) -> float:
        """
        Check rate limits before making a request

        Args:
            model: Model ID to check rate limits for
            tokens: Number of tokens to consume

        Returns:
            Wait time in seconds if rate limited, 0 otherwise
        """
        self.total_requests += 1

        # Check global rate limit first
        with self.global_rate_limit_lock:
            if self.global_rate_limited:
                now = time.time()
                if now < self.global_rate_limit_until:
                    wait_time = self.global_rate_limit_until - now
                    if wait_time > 0:
                        logger.info(f"Global rate limit active, waiting {wait_time:.2f}s")
                        self.total_limited += 1
                        self.total_wait_time += wait_time
                        return wait_time
                else:
                    # Reset global rate limit if time has passed
                    self.global_rate_limited = False

        # Add backoff if we've had errors with this model
        backoff = self._calculate_backoff(model)
        if backoff > 0:
            logger.info(f"Applying backoff for {model}: {backoff:.2f}s")
            self.total_limited += 1
            self.total_wait_time += backoff
            return backoff

        # If we've had many consecutive successful calls, skip local limiting
        if self.consecutive_successful_calls > 50 and not self.actual_rate_limits_detected:
            # Either API has very high limits or our rate limits are too conservative
            return 0.0

        # Check distributed rate limiter first if available
        if self.distributed_limiter:
            try:
                success, wait_time = self.distributed_limiter.consume(model, tokens)
                if not success:
                    logger.info(
                        f"Distributed rate limit reached for {model}, waiting {wait_time:.2f}s"
                    )
                    self.total_limited += 1
                    self.total_wait_time += wait_time
                    self.actual_rate_limits_detected = True
                    return wait_time
            except Exception as e:
                logger.warning(f"Error in distributed rate limiter: {e}")

        # If local limiting is disabled, skip it
        if not self.local_limiting_enabled:
            return 0.0

        # Fall back to local rate limiter
        local_limiter = self._get_local_limiter(model)
        success, wait_time = local_limiter.consume(tokens)

        if not success:
            # For long wait times, check if we should really wait or just proceed
            if wait_time > 30.0 and not self.actual_rate_limits_detected:
                logger.info(
                    f"Long local rate limit ({wait_time:.2f}s) detected but no actual API limits hit. Proceeding cautiously."
                )
                # Reset the limiter to allow some capacity
                local_limiter.tokens = max(tokens * 3, local_limiter.capacity * 0.2)
                return 0.0

            logger.info(f"Local rate limit reached for {model}, waiting {wait_time:.2f}s")
            self.total_limited += 1
            self.total_wait_time += wait_time
            return wait_time

        return 0.0

    def after_response(
        self,
        model: str,
        response_headers: Dict[str, str],
        status_code: int = 200,
        response_time: Optional[float] = None,
        wait_time: Optional[float] = None,
    ) -> None:
        """
        Adjust rate limits based on API responses

        Args:
            model: Model ID
            response_headers: API response headers
            status_code: HTTP status code of the response
            response_time: Time taken for the API call (seconds)
            wait_time: Optional explicit wait time from API
        """
        # Reset retry counter on successful response
        if 200 <= status_code < 300:
            self.retry_counts[model] = 0
            self.consecutive_successful_calls += 1

        # Increment retry counter on rate limit errors
        elif status_code == 429:  # Too Many Requests
            self.retry_counts[model] = self.retry_counts.get(model, 0) + 1

            # Set minimum wait time based on explicit wait time or calculate from headers
            min_wait_time = wait_time if wait_time is not None else 60
            logger.warning(
                f"Rate limit error for {model}, retry count: {self.retry_counts[model]}, "
                f"wait time: {min_wait_time}s"
            )

            # Mark that we've seen an actual rate limit
            self.actual_rate_limits_detected = True
            self.consecutive_successful_calls = 0

            # Adjust local rate limiter to be more conservative
            local_limiter = self._get_local_limiter(model)

            # Less aggressive reduction but longer enforced wait
            new_capacity = max(3, int(local_limiter.capacity * 0.7))

            # Update with a much slower fill rate based on API's required wait time
            new_fill_rate = new_capacity / (min_wait_time * 2)  # Very slow refill

            local_limiter.update_capacity(new_capacity, new_fill_rate)
            logger.warning(
                f"Updated rate limit for {model} to {new_capacity} requests per {min_wait_time*2} seconds"
            )

            # Force more tokens into the bucket to ensure a longer wait
            local_limiter.tokens = 0  # Empty the bucket to force waiting

            # Re-enable local limiting if it was disabled
            self.local_limiting_enabled = True

            # Store this rate limit in all local limiters to force global backoff
            for limiter_model, limiter in self.local_limiters.items():
                if limiter_model != model:
                    # Reduce other models too but less aggressively
                    limiter.tokens = min(limiter.tokens, limiter.capacity * 0.3)
                    logger.info(f"Reduced tokens for {limiter_model} due to rate limit on {model}")

        # Extract rate limit information from headers
        remaining = response_headers.get("x-ratelimit-remaining-requests")
        reset = response_headers.get("x-ratelimit-reset")
        limit = response_headers.get("x-ratelimit-limit-requests")

        if remaining and reset and limit:
            # Update rate limiters based on API feedback
            try:
                remaining = int(remaining)
                reset_seconds = int(reset)
                request_limit = int(limit)

                # If we're not close to the limit, consider disabling local limiting
                if remaining > 0.8 * request_limit and self.consecutive_successful_calls > 10:
                    self.local_limiting_enabled = False
                    logger.info(
                        "API limits not close to being reached. Disabling local rate limiting."
                    )

                # Update config for this model
                token_limit = self.config.get_model_limit(model)[1]
                self.config.add_model_limit(model, request_limit, token_limit)
                logger.info(
                    f"Updated rate limit config for {model} from API headers: limit={request_limit}, remaining={remaining}"
                )

                # Adjust local limiter
                if model in self.local_limiters:
                    # Calculate a more accurate fill rate
                    new_fill_rate = request_limit / 60.0

                    # Update capacity and tokens based on API feedback
                    limiter = self.local_limiters[model]
                    limiter.update_capacity(max(remaining, 1), new_fill_rate)
                    logger.debug(f"Updated rate limiter for {model} based on API headers")
            except (ValueError, TypeError) as e:
                logger.warning(f"Error parsing rate limit headers: {e}")

    def get_metrics(self) -> Dict[str, Any]:
        """Get metrics about rate limiter usage"""
        metrics = {
            "total_requests": self.total_requests,
            "total_limited": self.total_limited,
            "total_wait_time": self.total_wait_time,
            "average_wait_time": (
                self.total_wait_time / self.total_limited if self.total_limited > 0 else 0.0
            ),
            "models": {},
        }

        # Add per-model metrics
        for model, limiter in self.local_limiters.items():
            metrics["models"][model] = {
                "local": limiter.get_metrics(),
                "retry_count": self.retry_counts.get(model, 0),
                "response_time": self.response_times.get(model, 0),
            }

        # Add distributed metrics if available
        if self.distributed_limiter:
            metrics["distributed"] = self.distributed_limiter.get_metrics()

        return metrics

    def wait_if_needed(self, model: str, tokens: int = 1) -> None:
        """
        Check rate limits and wait if necessary

        Args:
            model: Model ID to check rate limits for
            tokens: Number of tokens to consume

        Raises:
            RateLimitExceededError: If max retries are exceeded
        """
        wait_time = self.before_request(model, tokens)
        if wait_time > 0:
            retry_count = self.retry_counts.get(model, 0)
            if retry_count >= self.config.max_retries:
                raise RateLimitExceededError(
                    wait_time, f"Max retries ({self.config.max_retries}) exceeded for {model}"
                )

            logger.info(f"Rate limited, waiting {wait_time:.2f}s before retrying")
            time.sleep(wait_time)
            # Try again after waiting
            return self.wait_if_needed(model, tokens)

    def set_global_rate_limit(self, wait_time: float) -> None:
        """Set a global rate limit for all models"""
        with self.global_rate_limit_lock:
            self.global_rate_limited = True
            self.global_rate_limit_until = time.time() + wait_time
            logger.warning(f"Global rate limit set for {wait_time:.2f} seconds")
