"""
TransPhrase - AI-powered web novel translation & phrasing tool

A Python application for translating web novels and other text content
using various language models with advanced features like caching,
rate limiting, and plugin support.
"""

__version__ = "0.1.0"

from transphrase.api.handler import APIHandler

# Public API
from transphrase.core.config import TranslationConfig
from transphrase.core.file_processor import FileProcessor
