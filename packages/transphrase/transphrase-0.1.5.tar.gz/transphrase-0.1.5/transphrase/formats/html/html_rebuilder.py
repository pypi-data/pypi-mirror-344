"""HTML rebuilding with translated content"""

import logging
import time
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup, NavigableString

logger = logging.getLogger("translator")


class HTMLRebuilder:
    """Rebuilds HTML with translations"""

    def __init__(self, processor):
        """
        Initialize HTML rebuilder

        Args:
            processor: Reference to the parent HTMLProcessor
        """
        self.processor = processor

    def rebuild_html(
        self, html_content: str, translations: List[str], mapping: Dict, entity_handler
    ) -> str:
        """
        Rebuild HTML with translated content

        Args:
            html_content: Original HTML content
            translations: List of translated text segments
            mapping: Mapping data for reconstruction
            entity_handler: Handler for HTML entities

        Returns:
            HTML with translated content
        """
        start_time = time.time()

        # Save original HTML for structure comparison
        original_html = html_content

        # Protect HTML entities if needed
        if self.processor.preserve_entities and not entity_handler.entity_map:
            html_content, entity_handler.entity_map = entity_handler.protect_entities(html_content)

        soup = BeautifulSoup(html_content, "html.parser")

        # Verify document structure hasn't changed
        from .html_extractor import ContentExtractor

        extractor = ContentExtractor(self.processor)
        current_hash = extractor._generate_structure_hash(soup)
        if mapping.get("metadata", {}).get("structure_hash") != current_hash:
            logger.warning("HTML structure has changed; translation may be imprecise")

        # First handle select/option elements specially
        self._rebuild_select_options(soup, translations, mapping)

        # Then replace attribute content
        for segment_index, attr_info in mapping.get("attributes", {}).items():
            try:
                selector = attr_info["selector"]
                attribute = attr_info["attribute"]

                # Find the tag using the selector
                matching_tag = soup.select_one(selector)

                if matching_tag and attribute in matching_tag.attrs:
                    translation = translations[int(segment_index)]
                    # Restore HTML entities if needed
                    if self.processor.preserve_entities:
                        translation = entity_handler.restore_entities(translation)
                    matching_tag[attribute] = translation
            except Exception as e:
                logger.warning(f"Failed to update attribute: {e}")

        # Then replace node content with better structure preservation
        for segment_index, node_info in mapping.get("nodes", {}).items():
            # Skip option tags as they're handled separately
            if (
                node_info.get("is_option", False)
                or "select_options" in mapping
                and segment_index in mapping["select_options"]
            ):
                continue

            try:
                selector = node_info["selector"]
                node_map = node_info.get("node_map", {})
                original = node_info.get("original", "")
                translation = translations[int(segment_index)]

                # Skip if translation is empty
                if not translation.strip():
                    continue

                # Restore HTML entities
                if self.processor.preserve_entities:
                    translation = entity_handler.restore_entities(translation)

                # Replace content with structure preservation
                if node_map:
                    translation = self._rebuild_with_inline_tags(translation, node_map)

                # Find the element using the selector
                matching_tag = soup.select_one(selector)
                if matching_tag:
                    # Replace the content
                    self._replace_tag_content_with_structure(matching_tag, translation)
            except Exception as e:
                logger.warning(f"Failed to update node content: {e}")

        # Fix any issues with select/option structure
        self._validate_and_fix_select_options(soup)

        # Convert back to string
        html_result = str(soup)

        # Restore any remaining HTML entities
        if self.processor.preserve_entities:
            html_result = entity_handler.restore_entities(html_result)

        # Validate structure and fix issues
        from .html_validation import StructureValidator

        validator = StructureValidator()
        is_valid, message = validator.validate_structure(original_html, html_result)
        if not is_valid:
            logger.warning(f"HTML structure validation failed: {message}")
            html_result = validator.fix_critical_issues(html_result, original_html)

        # Log performance metrics
        processing_time = time.time() - start_time
        logger.debug(f"HTML rebuilding took {processing_time:.3f}s")

        return html_result

    def _rebuild_select_options(self, soup, translations, mapping):
        """Specially rebuild select elements and their options to preserve structure"""
        # Implementation from the original file
        # ...
        # Process each select option directly
        for segment_index, option_info in mapping.get("select_options", {}).items():
            try:
                select_selector = option_info.get("select_selector")
                option_selector = option_info.get("option_selector")
                option_idx = option_info.get("option_index", 0)

                # Get translation
                translation = translations[int(segment_index)]
                if self.processor.preserve_entities:
                    # Use entity handler from the processor
                    translation = self.processor.entity_handler.restore_entities(translation)

                # Try multiple strategies to locate the correct option element
                option_tag = None

                # Strategy 1: Direct selector
                if option_selector:
                    option_tag = soup.select_one(option_selector)

                # Strategy 2: Find by index within parent select
                if not option_tag and select_selector:
                    select_tag = soup.select_one(select_selector)
                    if select_tag:
                        options = select_tag.find_all("option")
                        if options and option_idx < len(options):
                            option_tag = options[option_idx]

                # Strategy 3: Find any select and use the option index
                if not option_tag:
                    all_selects = soup.find_all("select")
                    for sel in all_selects:
                        options = sel.find_all("option")
                        if options and option_idx < len(options):
                            option_tag = options[option_idx]
                            break

                # If option is found, update it correctly
                if option_tag:
                    # Important: completely replace the content rather than just setting string
                    # to ensure proper structure
                    option_tag.clear()
                    option_tag.string = translation

                    # Preserve all original attributes
                    attrs = option_info.get("attributes", {})
                    for attr_name, attr_value in attrs.items():
                        option_tag[attr_name] = attr_value

                # If option not found, we need to create it
                elif translation.strip():
                    # Find a select to add this option to
                    target_select = (
                        soup.select_one(select_selector) if select_selector else soup.find("select")
                    )
                    if target_select:
                        new_option = soup.new_tag("option")
                        new_option.string = translation

                        # Add any attributes from the original option
                        for attr_name, attr_value in option_info.get("attributes", {}).items():
                            new_option[attr_name] = attr_value

                        target_select.append(new_option)

            except Exception as e:
                logger.warning(f"Failed to update select option (index {segment_index}): {e}")

        # Extra step: Clean up any text nodes directly inside select elements
        # These should be inside option elements instead
        for select in soup.find_all("select"):
            for child in list(select.children):
                if isinstance(child, NavigableString) and child.strip():
                    # Create a new option for this orphaned text
                    new_option = soup.new_tag("option")
                    new_option.string = child.string
                    child.replace_with(new_option)

        # Final cleanup: ensure no option tags exist outside of select elements
        for orphan_option in soup.find_all("option"):
            if not orphan_option.parent or orphan_option.parent.name != "select":
                orphan_option.extract()  # Remove from current location

                # Try to find a select to add it to
                target_select = soup.find("select")
                if target_select:
                    target_select.append(orphan_option)
                else:
                    # If no select exists, create one
                    new_select = soup.new_tag("select")
                    new_select["class"] = "toc"
                    orphan_option.wrap(new_select)

                    # Find a good place to insert this select
                    body = soup.find("body")
                    if body:
                        body.append(new_select)
                    else:
                        soup.append(new_select)

    def _validate_and_fix_select_options(self, soup):
        """Validate and fix select/option structures in the HTML"""
        # Implementation from the original file
        # ...
        # 1. Find and collect all option elements, wherever they are
        all_options = []
        for option in soup.find_all("option"):
            # Check if option is not properly inside a select
            if not option.parent or option.parent.name != "select":
                all_options.append(option)
                option.extract()  # Remove from current position

        # 2. Find text directly under select (should be in options)
        for select in soup.find_all("select"):
            for child in list(select.children):
                if isinstance(child, NavigableString) and child.strip():
                    # This text should be in an option
                    new_option = soup.new_tag("option")
                    new_option.string = child.string
                    child.replace_with(new_option)

        # 3. Ensure all selects have proper option children
        for select in soup.find_all("select"):
            options = select.find_all("option")
            if not options and all_options:
                # Add orphaned options to this select
                for option in all_options:
                    select.append(option)
                all_options = []  # Clear the list as we've used them

        # 4. If we still have orphaned options, create a new select for them
        if all_options:
            new_select = soup.new_tag("select")
            new_select["class"] = "toc"
            for option in all_options:
                new_select.append(option)

            # Find a good place to insert this select
            body = soup.find("body")
            if body:
                body.append(new_select)
            else:
                soup.append(new_select)

    def _rebuild_with_inline_tags(self, text, node_map):
        """
        Rebuild text with inline tags from node map.

        This method reinserts HTML formatting tags (like <b>, <i>, etc.) into translated text
        based on the node map that was created during extraction.

        Args:
            text: Translated text without formatting tags
            node_map: Dictionary mapping tag positions and types

        Returns:
            Text with inline formatting tags restored
        """
        try:
            # Early return for empty input or missing node map
            if not text or not node_map:
                return text

            # Create a list to collect parts of the result
            result_parts = []

            # Extract info from node_map
            # Node map typically contains tag positions like:
            # {"tags": [{"tag": "b", "start": 5, "end": 10}, ...]}
            tags_info = node_map.get("tags", [])

            # Sort tags by their start position to process in order
            sorted_tags = sorted(tags_info, key=lambda x: x.get("start", 0))

            # Track the current position in the text
            current_pos = 0
            open_tags = []

            for tag_info in sorted_tags:
                tag_name = tag_info.get("tag", "")
                start_pos = tag_info.get("start", 0)
                end_pos = tag_info.get("end", len(text))
                attributes = tag_info.get("attrs", {})

                # Skip invalid tags
                if not tag_name or start_pos >= len(text) or start_pos < 0:
                    continue

                # Check if this is a closing tag or opening tag
                is_closing = tag_info.get("is_closing", False)

                if is_closing:
                    # Handle closing tag
                    if open_tags and open_tags[-1]["tag"] == tag_name:
                        # Add text up to this point
                        result_parts.append(text[current_pos:start_pos])

                        # Add closing tag
                        result_parts.append(f"</{tag_name}>")

                        # Update position and remove tag from open tags
                        current_pos = start_pos
                        open_tags.pop()
                else:
                    # Handle opening tag
                    # Add text up to the tag
                    result_parts.append(text[current_pos:start_pos])

                    # Build tag with attributes
                    tag_str = f"<{tag_name}"
                    for attr_name, attr_value in attributes.items():
                        tag_str += f' {attr_name}="{attr_value}"'
                    tag_str += ">"

                    result_parts.append(tag_str)

                    # Track this tag as open
                    open_tags.append({"tag": tag_name, "end": end_pos})

                    # Update position
                    current_pos = start_pos

                    # If there's an end position, handle paired tags
                    if end_pos > start_pos and end_pos <= len(text):
                        # Add content between tags
                        result_parts.append(text[start_pos:end_pos])

                        # Add closing tag
                        result_parts.append(f"</{tag_name}>")

                        # Update position
                        current_pos = end_pos

                        # Remove from open tags since we closed it
                        if open_tags and open_tags[-1]["tag"] == tag_name:
                            open_tags.pop()

            # Add any remaining text
            if current_pos < len(text):
                result_parts.append(text[current_pos:])

            # Close any remaining open tags
            for tag in reversed(open_tags):
                result_parts.append(f"</{tag['tag']}>")

            return "".join(result_parts)
        except Exception as e:
            logger.warning(f"Error rebuilding text with inline tags: {e}")
            return text  # Return original text on error

    def _replace_tag_content_with_structure(self, tag, content):
        """
        Replace tag content while preserving structure.

        This method carefully replaces the content of a BeautifulSoup tag,
        preserving attributes, child structure, and inline formatting.

        Args:
            tag: BeautifulSoup tag to modify
            content: New content (HTML string) to place in the tag
        """
        if not tag:
            return

        try:
            # Clear existing contents while preserving the tag itself
            tag.clear()

            # If content contains HTML, parse it and add the result
            if "<" in content and ">" in content:
                # Create a temporary soup to parse the content
                from bs4 import BeautifulSoup

                temp_soup = BeautifulSoup(f"<div>{content}</div>", "html.parser")

                # Check if we got valid parsed content
                if temp_soup and temp_soup.div:
                    # Transfer each child from temp_soup to the original tag
                    for child in list(temp_soup.div.children):
                        tag.append(child)
                else:
                    # Fallback: add as string
                    tag.string = content
            else:
                # Simple text content
                tag.string = content

        except Exception as e:
            logger.warning(f"Error replacing tag content: {e}")
            # Fallback: try direct string replacement
            try:
                tag.string = content
            except Exception:
                # Last resort: just replace with a string node
                tag.replace_with(NavigableString(content))
