"""
TransPhrase - AI-powered web novel translation & phrasing tool

A Python application for translating web novels and other text content
using various language models with advanced features like caching,
rate limiting, and plugin support.
"""

__version__ = "0.1.0"
__all__ = ["TranslationConfig", "MainProcessor", "APIHandler"]

# Import deferred to prevent circular dependencies
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transphrase.api.handler import APIHandler
    from transphrase.core.config import TranslationConfig
    from transphrase.core.processing.main_processor import MainProcessor
