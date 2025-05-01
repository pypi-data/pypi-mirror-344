"""Text processing operations for translation"""

import logging
import re
from typing import List

from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString
from rich.progress import Progress, TaskID

from transphrase.api.handler import APIHandler

logger = logging.getLogger("translator")


class TextProcessor:
    """Handles text processing operations for translation"""

    def __init__(self, api_handler: APIHandler):
        """
        Initialize text processor

        Args:
            api_handler: API handler for translation
        """
        self.api_handler = api_handler

    def _process_chunk(
        self, chunk: str, system_prompt: str, model: str, progress: Progress, chunk_task_id: TaskID
    ) -> str:
        """Process a single chunk of text"""
        result = self.api_handler.translate_chunk(system_prompt, chunk, model)
        return result

    def is_html_content(self, text: str) -> bool:
        """Check if the given text contains HTML content.

        Args:
            text: The text to check for HTML tags

        Returns:
            bool: True if HTML tags are found, False otherwise
        """
        try:
            return bool(re.search(r"<[^>]+>", text))
        except (TypeError, re.error) as e:
            logger.error(f"Error checking HTML content: {e}")
            return False

    def split_html_semantic(self, html: str, max_chunk_size: int = 5000) -> List[str]:
        """Split HTML content into semantic chunks while preserving structure."""
        if not isinstance(html, str):
            raise TypeError("Input must be a string")
        if max_chunk_size < 1:
            raise ValueError("max_chunk_size must be at least 1")

        try:
            soup = BeautifulSoup(html, "html.parser")
            chunks: List[str] = []
            current_chunk = BeautifulSoup("", "html.parser")
            current_size = 0

            def process_element(element) -> None:
                """Process an HTML element and add it to the current chunk."""
                nonlocal current_chunk, current_size

                # Handle NavigableString objects (text nodes)
                if isinstance(element, NavigableString):
                    text_str = str(element)
                    text_size = len(text_str)

                    if current_size + text_size > max_chunk_size:
                        chunks.append(str(current_chunk))
                        current_chunk = BeautifulSoup("", "html.parser")
                        current_size = 0

                    # Create a new NavigableString instead of using copy()
                    current_chunk.append(NavigableString(text_str))
                    current_size += text_size
                    return

                # From here on, element is a Tag
                element_str = str(element)
                element_size = len(element_str)

                # Handle special elements that should remain intact
                if element.name in ["script", "style", "link", "meta"]:
                    if current_size + element_size > max_chunk_size:
                        chunks.append(str(current_chunk))
                        current_chunk = BeautifulSoup("", "html.parser")
                        current_size = 0
                    current_chunk.append(element)
                    current_size += element_size
                    return

                # Handle text content within elements
                if element.string and not element.contents:
                    text_chunks = self.split_text_semantic(element.string, max_chunk_size)
                    for chunk in text_chunks:
                        if current_size + len(chunk) > max_chunk_size:
                            chunks.append(str(current_chunk))
                            current_chunk = BeautifulSoup("", "html.parser")
                            current_size = 0
                        new_tag = current_chunk.new_tag(element.name, **element.attrs)
                        new_tag.string = chunk
                        current_chunk.append(new_tag)
                        current_size += len(chunk)
                    return

                # Handle nested elements
                if element.contents:
                    new_element = current_chunk.new_tag(element.name, **element.attrs)
                    for child in element.contents:
                        child_soup = BeautifulSoup("", "html.parser")
                        process_element(child)
                        new_element.append(child_soup)
                    if current_size + len(str(new_element)) > max_chunk_size:
                        chunks.append(str(current_chunk))
                        current_chunk = BeautifulSoup("", "html.parser")
                        current_size = 0
                    current_chunk.append(new_element)
                    current_size += len(str(new_element))
                    return

                # Default case for other elements
                if current_size + element_size > max_chunk_size:
                    chunks.append(str(current_chunk))
                    current_chunk = BeautifulSoup("", "html.parser")
                    current_size = 0
                current_chunk.append(element)
                current_size += element_size

            # Process each top-level element
            for element in soup.contents:
                process_element(element)

            # Add final chunk if not empty
            if len(str(current_chunk)) > 0:
                chunks.append(str(current_chunk))

            # Ensure each chunk has complete HTML structure
            complete_chunks = []
            for chunk in chunks:
                soup_chunk = BeautifulSoup(chunk, "html.parser")
                if not soup_chunk.find("html"):
                    # Create minimal HTML structure if missing
                    html_tag = soup_chunk.new_tag("html")
                    body_tag = soup_chunk.new_tag("body")
                    body_tag.append(soup_chunk)
                    html_tag.append(body_tag)
                    soup_chunk = BeautifulSoup(str(html_tag), "html.parser")
                complete_chunks.append(str(soup_chunk))

            return complete_chunks

        except Exception as e:
            logger.error(f"Error parsing HTML content: {e}")
            raise ValueError("Failed to parse HTML content") from e

    def split_text_semantic(self, text: str, max_chunk_size: int = 5000) -> List[str]:
        """Split text into semantic chunks respecting sentence boundaries.

        Args:
            text: The text to split
            max_chunk_size: Maximum size of each chunk

        Returns:
            List[str]: List of text chunks
        """
        if len(text) <= max_chunk_size:
            return [text]

        # Handle HTML content differently
        if self.is_html_content(text):
            return self.split_html_semantic(text, max_chunk_size)

        # Define sentence boundaries
        sentence_endings = r"(?<=[.!?])\s+"
        sentences = re.split(sentence_endings, text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            # If a single sentence is too long, split it by comma or semicolon
            if len(sentence) > max_chunk_size:
                phrase_endings = r"(?<=[,;])\s+"
                phrases = re.split(phrase_endings, sentence)

                for phrase in phrases:
                    if len(current_chunk) + len(phrase) + 2 <= max_chunk_size:
                        current_chunk += phrase + " "
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())

                        # If a single phrase is still too long, force split
                        if len(phrase) > max_chunk_size:
                            # Split into fixed-size chunks, preserving words
                            words = phrase.split()
                            phrase_chunk = ""

                            for word in words:
                                if len(phrase_chunk) + len(word) + 1 <= max_chunk_size:
                                    phrase_chunk += word + " "
                                else:
                                    chunks.append(phrase_chunk.strip())
                                    phrase_chunk = word + " "

                            if phrase_chunk:
                                current_chunk = phrase_chunk
                        else:
                            current_chunk = phrase + " "

            # Normal case - sentence fits or can be added
            elif len(current_chunk) + len(sentence) + 2 <= max_chunk_size:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        # Add the last chunk if not empty
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _split_text(self, text, max_chunk_size=None):
        """
        Split text into chunks based on paragraph boundaries

        Args:
            text: Text to split
            max_chunk_size: Maximum size for each chunk

        Returns:
            List of text chunks
        """
        # Use provided max_chunk_size or default value
        chunk_size = max_chunk_size or 4000

        # Use the semantic splitter for all text
        return self.split_text_semantic(text, max_chunk_size=chunk_size)
