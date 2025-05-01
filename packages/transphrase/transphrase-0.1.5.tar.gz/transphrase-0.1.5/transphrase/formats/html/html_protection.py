"""HTML structure protection for translation"""

import logging
import re
from functools import lru_cache
from typing import Callable, Dict, List, Tuple

logger = logging.getLogger("translator")


class StructureProtector:
    """Optimized HTML structure protection for translation"""

    def __init__(self):
        """Initialize with compiled regex patterns for better performance"""
        # Precompile regex patterns
        self.select_pattern = re.compile(r"(<select[^>]*>.*?</select>)", re.DOTALL)
        self.script_style_pattern = re.compile(
            r"(<(?:script|style)[^>]*>.*?</(?:script|style)>)", re.DOTALL
        )
        self.comment_pattern = re.compile(r"(<!--.*?-->)", re.DOTALL)
        self.tag_pattern = re.compile(r"<[^>]+>")
        self.markdown_block_pattern = re.compile(r"```\w*\s*|```\s*")
        self.backtick_pattern = re.compile(r"^\s*`+\s*|\s*`+\s*$")
        self.option_cleanup_pattern = re.compile(r"(</option>)\s*([^<]*?)\s*(<option)", re.DOTALL)
        self.option_content_fix_pattern = re.compile(
            r"(<option[^>]*>)\s*</option>\s*([^<]+?)(?=<option|</select>)"
        )
        # New patterns for paragraph handling
        self.text_block_pattern = re.compile(r"\n\n+")
        self.paragraph_pattern = re.compile(r"<p>(.*?)</p>", re.DOTALL)
        self.body_pattern = re.compile(r"<body>(.*?)</body>", re.DOTALL)
        self.standalone_text_pattern = re.compile(r">([^<]{50,})<", re.DOTALL)

    @lru_cache(maxsize=128)
    def _create_placeholder(self, idx: int, type_prefix: str) -> str:
        """Create a placeholder with caching for better performance"""
        return f"__{type_prefix}_{idx}__"

    def translate_with_protection(
        self, html_content: str, translate_func: Callable[[str], str]
    ) -> str:
        """
        Optimized HTML translation with complete structure preservation

        Args:
            html_content: Original HTML content
            translate_func: Function to translate text content

        Returns:
            Translated HTML content
        """
        # Step 1: Apply parallel processing for large documents
        if len(html_content) > 100000:  # For very large HTML documents
            return self._translate_large_html(html_content, translate_func)

        # Step 2: Fast protection of structural elements using precompiled patterns
        mappings = {"select": {}, "script_style": {}, "comment": {}, "tag": {}, "body": {}}

        # Save original body content to check for paragraph structure later
        body_match = self.body_pattern.search(html_content)
        original_body = body_match.group(1) if body_match else None
        original_p_count = len(self.paragraph_pattern.findall(html_content))

        # Process in a single pass, storing replacements for later
        for pattern_type, pattern in [
            ("select", self.select_pattern),
            ("script_style", self.script_style_pattern),
            ("comment", self.comment_pattern),
        ]:
            for idx, match in enumerate(pattern.findall(html_content)):
                placeholder = self._create_placeholder(idx, pattern_type.upper())
                mappings[pattern_type][placeholder] = match
                html_content = html_content.replace(match, placeholder)

        # Process tags in a single pass with optimized replacement
        tags = self.tag_pattern.findall(html_content)
        for idx, tag in enumerate(tags):
            placeholder = self._create_placeholder(idx, "TAG")
            mappings["tag"][placeholder] = tag
            # Use a more efficient string replacement for the first occurrence
            pos = html_content.find(tag)
            if pos >= 0:
                html_content = html_content[:pos] + placeholder + html_content[pos + len(tag) :]

        # Step 3: Translate the simplified content
        translated_content = translate_func(html_content)

        # Step 4: Remove any markdown code block markers that might have been added
        translated_content = self._remove_markdown_blocks(translated_content)

        # Step 5: Restore placeholders in reverse order (more efficient)
        # Restore tags first
        for placeholder, tag in mappings["tag"].items():
            translated_content = translated_content.replace(placeholder, tag)

        # Then restore other elements
        for element_type in ["comment", "script_style", "select"]:
            for placeholder, content in mappings[element_type].items():
                translated_content = translated_content.replace(placeholder, content)

        # Step 6: Check for long text not in paragraph tags
        translated_content = self._wrap_standalone_text(translated_content)

        # Step 7: Remove any remaining markdown markers that might have survived
        translated_content = self._remove_markdown_blocks(translated_content)

        # Step 8: Fix specific issues with option tags
        translated_content = self._fix_option_tags(translated_content)

        return translated_content

    def _remove_markdown_blocks(self, content: str) -> str:
        """Remove markdown code block markers from content"""
        # Remove opening code block markers like ```html
        content = re.sub(r"```\w*\s*", "", content)

        # Remove closing code block markers
        content = re.sub(r"```\s*", "", content)

        # Remove other backtick markers that might interfere
        content = re.sub(r"^\s*`+\s*", "", content)
        content = re.sub(r"\s*`+\s*$", "", content)

        return content

    def _wrap_standalone_text(self, content: str) -> str:
        """Wrap substantial standalone text in paragraph tags"""

        def wrap_match(match):
            text = match.group(1)
            # Only wrap if it's substantial text
            if len(text.strip()) > 50:
                return f"><p>{text}</p><"
            return f">{text}<"

        return self.standalone_text_pattern.sub(wrap_match, content)

    def _fix_option_tags(self, content: str) -> str:
        """Fix issues with option tags"""
        # Fix malformed select-option pairs
        content = re.sub(r"(<select[^>]*>)\s*([^<]*?)(<option)", r"\1\3", content)
        content = re.sub(r"(</option>)\s*([^<]*?)(<option|</select>)", r"\1\3", content)

        # Fix option tags without proper closing
        content = re.sub(r"(<option[^>]*>)([^<]*?)(<option)", r"\1\2</option>\3", content)

        # Fix option values getting split
        content = re.sub(
            r'(<option\s+value=")([^"]*?)("\s*>)(.*?)(</option>)',
            lambda m: f"{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4) if m.group(4) else m.group(2)}{m.group(5)}",
            content,
        )

        # Fix malformed option tags
        content = re.sub(r'<option value="([^"]*)"<select', r'<option value="\1">', content)

        return content

    def _translate_large_html(self, html_content: str, translate_func: Callable[[str], str]) -> str:
        """Process large HTML documents by chunking them intelligently"""
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html_content, "html.parser")

            # Find all text nodes with substantial content
            for text_node in soup.find_all(text=True):
                # Skip if inside a script or style tag
                if text_node.parent.name in ["script", "style"]:
                    continue

                # Skip if it's just whitespace
                if not text_node.strip():
                    continue

                # Translate text node
                translated_text = translate_func(text_node)

                # Remove any markdown markers
                translated_text = self._remove_markdown_blocks(translated_text)

                # Replace original text
                text_node.replace_with(translated_text)

            # Return the processed HTML
            return str(soup)

        except Exception as e:
            logger.error(f"Error processing large HTML file: {str(e)}")
            # Fall back to basic processing
            return self.translate_with_protection(html_content, translate_func)

    def process_large_html(
        self,
        input_path: str,
        translate_callback,
        max_chunk_size: int = 100000,
        output_path: str = None,
    ) -> str:
        """Process a large HTML file in chunks with structure preservation"""
        # Read the input file
        with open(input_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Process using BeautifulSoup for better structure preservation
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html_content, "html.parser")

            # Collect text nodes to translate
            text_nodes = []
            for text_node in soup.find_all(text=True):
                # Skip if inside a script, style or select tag
                if text_node.parent.name in ["script", "style", "select", "noscript"]:
                    continue

                # Skip if it's just whitespace
                if not text_node.strip():
                    continue

                text_nodes.append((text_node, text_node.string))

            # Group nodes into batches for efficiency
            text_batches = []
            current_batch = []
            current_size = 0

            for node, text in text_nodes:
                if current_size + len(text) > max_chunk_size:
                    if current_batch:  # Only append if batch has items
                        text_batches.append(current_batch)
                        current_batch = []
                        current_size = 0

                current_batch.append((node, text))
                current_size += len(text)

            # Add final batch if not empty
            if current_batch:
                text_batches.append(current_batch)

            # Process each batch
            for batch in text_batches:
                # Extract just the text
                texts = [text for _, text in batch]

                # Translate batch
                translated_texts = translate_callback(texts)

                # Update nodes with translations
                for i, ((node, _), translated_text) in enumerate(zip(batch, translated_texts)):
                    # Clean any markdown markers
                    cleaned_text = self._remove_markdown_blocks(translated_text)
                    node.string.replace_with(cleaned_text)

            # Get the processed HTML
            result = str(soup)

            # Write to output file if specified
            if output_path:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result)

            return result

        except Exception as e:
            logger.error(f"Error processing large HTML file: {str(e)}")
            # Fall back to simpler processing
            result = self._translate_large_html(html_content, lambda x: translate_callback([x])[0])

            # Write to output file if specified
            if output_path:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result)

            return result
