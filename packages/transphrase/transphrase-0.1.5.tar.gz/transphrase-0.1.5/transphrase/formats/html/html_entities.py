"""HTML entity handling for translation"""

import re
from functools import lru_cache
from typing import Dict, Tuple


class EntityHandler:
    """Handles HTML entity protection and restoration"""

    def __init__(self, cache_size: int = 128):
        """
        Initialize entity handler

        Args:
            cache_size: Size of LRU cache for entity processing
        """
        self.cache_size = cache_size
        self.entity_map = {}
        self._protect_entities = lru_cache(maxsize=cache_size)(self._protect_entities_impl)

    def protect_entities(self, html_content: str) -> Tuple[str, Dict[str, str]]:
        """
        Protect HTML entities by replacing them with placeholders

        Args:
            html_content: Original HTML content

        Returns:
            Tuple of (modified HTML content, entity mapping)
        """
        return self._protect_entities(html_content)

    def _protect_entities_impl(self, html_content: str) -> Tuple[str, Dict[str, str]]:
        """
        Implementation of HTML entity protection

        Args:
            html_content: Original HTML content

        Returns:
            Tuple of (modified HTML content, entity mapping)
        """
        entity_map = {}

        # Find HTML entities - optimized regex pattern
        entity_pattern = re.compile(r"&[a-zA-Z0-9#][a-zA-Z0-9]*;")

        # Find all entities at once and create mapping
        for i, entity in enumerate(entity_pattern.findall(html_content)):
            placeholder = f"__ENTITY_{i}__"
            entity_map[placeholder] = entity

        # Replace all at once for better performance
        for placeholder, entity in entity_map.items():
            html_content = html_content.replace(entity, placeholder)

        return html_content, entity_map

    def restore_entities(self, content: str) -> str:
        """
        Restore HTML entities from placeholders

        Args:
            content: Content with entity placeholders

        Returns:
            Content with restored HTML entities
        """
        if not self.entity_map:
            return content

        # Replace all entities at once
        for placeholder, entity in self.entity_map.items():
            content = content.replace(placeholder, entity)

        return content
