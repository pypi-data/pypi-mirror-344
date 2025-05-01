"""HTML processing modules for translation"""

from transphrase.core.processing.html_processor import HTMLProcessor

from .html_entities import EntityHandler
from .html_extractor import ContentExtractor
from .html_protection import StructureProtector
from .html_rebuilder import HTMLRebuilder
from .html_validation import StructureValidator

__all__ = [
    "HTMLProcessor",
    "EntityHandler",
    "ContentExtractor",
    "HTMLRebuilder",
    "StructureProtector",
    "StructureValidator",
]
