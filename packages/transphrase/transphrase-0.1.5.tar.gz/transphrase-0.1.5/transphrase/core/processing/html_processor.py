"""HTML processing operations for translation"""

import logging
import re
import time
from functools import lru_cache
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple

from bs4 import BeautifulSoup, NavigableString, Tag

from transphrase.formats.html.html_entities import EntityHandler
from transphrase.formats.html.html_extractor import ContentExtractor
from transphrase.formats.html.html_protection import StructureProtector
from transphrase.formats.html.html_rebuilder import HTMLRebuilder
from transphrase.formats.html.html_validation import StructureValidator

logger = logging.getLogger("translator")


class HTMLProcessor:
    """Handles HTML processing for translation"""

    # Tags whose text content should be translated
    TRANSLATABLE_TAGS = [
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "p",
        "a",
        "span",
        "div",
        "li",
        "td",
        "th",
        "button",
        "label",
        "title",
        "figcaption",
    ]

    # Tags that should be ignored
    IGNORE_TAGS = ["script", "style", "code", "pre", "noscript", "option", "select"]

    # Tags to ignore when extracting content
    IGNORE_EXTRACTING_FROM = ["script", "style", "code", "pre", "noscript", "select", "option"]

    # Tags that should be preserved during translation (formatting tags)
    PRESERVED_INLINE_TAGS = ["strong", "em", "b", "i", "u", "mark", "sub", "sup", "small", "br"]

    # Attributes that should be translated
    TRANSLATABLE_ATTRS = ["title", "alt", "placeholder", "aria-label"]

    def __init__(self, preserve_entities: bool = True, cache_size: int = 128):
        """
        Initialize HTML processor

        Args:
            preserve_entities: Whether to preserve HTML entities
            cache_size: Size of LRU cache for entity processing
        """
        self.preserve_entities = preserve_entities
        self.cache_size = cache_size

        # Initialize component handlers
        self.entity_handler = EntityHandler(cache_size)
        self.extractor = ContentExtractor(self)
        self.rebuilder = HTMLRebuilder(self)
        self.protector = StructureProtector()
        self.validator = StructureValidator()

    def extract_translatable_content(self, html_content: str) -> Tuple[List[str], Dict]:
        """
        Extract text content from HTML that should be translated.

        Args:
            html_content: The HTML content as string

        Returns:
            Tuple containing:
            - List of text segments to translate
            - Mapping data for reconstruction
        """
        # Measure start time for performance tracking
        start_time = time.time()

        # Protect HTML entities if configured
        if self.preserve_entities:
            html_content, entity_map = self.entity_handler.protect_entities(html_content)
            self.entity_handler.entity_map = entity_map

        # Use the extractor to get segments and mapping
        segments, mapping = self.extractor.extract_content(html_content)

        # Log performance metrics
        processing_time = time.time() - start_time
        logger.debug(f"HTML extraction took {processing_time:.3f}s, found {len(segments)} segments")

        return segments, mapping

    def rebuild_html_with_translations(
        self, html_content: str, translations: List[str], mapping: Dict
    ) -> str:
        """
        Rebuild HTML with translated content.

        Args:
            html_content: Original HTML content
            translations: List of translated text segments
            mapping: Mapping data for reconstruction

        Returns:
            HTML with translated content
        """
        return self.rebuilder.rebuild_html(html_content, translations, mapping, self.entity_handler)

    def translate_html_with_protection(self, html_content: str, translate_func) -> str:
        """
        Translate HTML content with complete structure preservation

        Args:
            html_content: Original HTML content
            translate_func: Function to translate text content

        Returns:
            Translated HTML content
        """
        return self.protector.translate_with_protection(html_content, translate_func)

    def process_large_html(
        self,
        input_path: str,
        translate_callback,
        max_chunk_size: int = 100000,
        output_path: str = None,
    ) -> str:
        """
        Process a large HTML file in chunks while preserving structure.

        Delegates to the StructureProtector's process_large_html method.

        Args:
            input_path: Path to the HTML file to process
            translate_callback: Function that translates text segments
            max_chunk_size: Maximum size of text chunks to process at once
            output_path: Optional path to write the output file

        Returns:
            Processed HTML content
        """
        # Delegate to the protector's implementation
        return self.protector.process_large_html(
            input_path=input_path,
            translate_callback=translate_callback,
            max_chunk_size=max_chunk_size,
            output_path=output_path,
        )
