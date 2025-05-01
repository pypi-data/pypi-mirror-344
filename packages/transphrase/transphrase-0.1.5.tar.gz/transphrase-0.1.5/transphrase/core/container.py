"""Dependency injection container for TransPhrase.

This module provides a container class that manages the initialization and
lifecycle of application dependencies using dependency injection.
"""

from dataclasses import dataclass
from typing import Optional

from transphrase.api.handler import APIHandler
from transphrase.cache.translation_cache import TranslationCache
from transphrase.core.config import TranslationConfig
from transphrase.core.processing.main_processor import MainProcessor
from transphrase.database.models import DBManager
from transphrase.rate_limiting.rate_limiter import AdaptiveRateLimiter


@dataclass
class Container:
    """Container for application dependencies.

    Attributes:
        config: The application configuration
        api_handler: API handler for translation requests
        cache: Translation cache for storing results
        db_manager: Database manager for persistent storage
        rate_limiter: Rate limiter for API requests
        file_processor: Main processor for handling file operations
    """

    config: TranslationConfig
    api_handler: Optional[APIHandler] = None
    cache: Optional[TranslationCache] = None
    db_manager: Optional[DBManager] = None
    rate_limiter: Optional[AdaptiveRateLimiter] = None
    file_processor: Optional[MainProcessor] = None

    def __post_init__(self) -> None:
        """Initialize dependencies.

        This method initializes all dependencies that weren't explicitly provided.
        It follows a specific order to ensure proper dependency injection:
        1. Cache
        2. Rate limiter
        3. Database manager
        4. API handler
        5. File processor
        """
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
            self.file_processor = MainProcessor(
                config=self.config, api_handler=self.api_handler, db_manager=self.db_manager
            )
