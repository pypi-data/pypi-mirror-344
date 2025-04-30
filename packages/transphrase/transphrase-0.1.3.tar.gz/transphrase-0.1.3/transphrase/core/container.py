"""Dependency injection container for TransPhrase."""

from dataclasses import dataclass
from typing import Optional

from transphrase.api.handler import APIHandler
from transphrase.cache.translation_cache import TranslationCache
from transphrase.core.config import TranslationConfig
from transphrase.core.file_processor import FileProcessor
from transphrase.database.models import DBManager
from transphrase.rate_limiting.rate_limiter import AdaptiveRateLimiter


@dataclass
class Container:
    """Container for application dependencies."""

    config: TranslationConfig
    api_handler: Optional[APIHandler] = None
    cache: Optional[TranslationCache] = None
    db_manager: Optional[DBManager] = None
    rate_limiter: Optional[AdaptiveRateLimiter] = None
    file_processor: Optional[FileProcessor] = None

    def __post_init__(self):
        """Initialize dependencies."""
        if self.cache is None and self.config.use_cache:
            self.cache = TranslationCache(ttl=self.config.cache_ttl)

        if self.rate_limiter is None:
            self.rate_limiter = AdaptiveRateLimiter(config=self.config.rate_limit_config)

        if self.db_manager is None:
            self.db_manager = DBManager(self.config.db_path)

        if self.api_handler is None:
            self.api_handler = APIHandler(
                api_key=self.config.api_key,
                base_url=self.config.base_url,
                cache=self.cache,
                rate_limiter=self.rate_limiter,
            )

        if self.file_processor is None:
            self.file_processor = FileProcessor(
                config=self.config, api_handler=self.api_handler, db_manager=self.db_manager
            )
