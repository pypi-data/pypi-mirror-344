"""HTML content extraction for translation"""

import hashlib
from typing import Any, Dict, List, Tuple

from bs4 import BeautifulSoup, NavigableString, Tag


class ContentExtractor:
    """Extracts translatable content from HTML"""

    def __init__(self, processor):
        """
        Initialize content extractor

        Args:
            processor: Reference to the parent HTMLProcessor
        """
        self.processor = processor

    def extract_content(self, html_content: str) -> Tuple[List[str], Dict]:
        """
        Extract translatable content from HTML

        Args:
            html_content: HTML content as string

        Returns:
            Tuple of (segments, mapping)
        """
        # Parse HTML with a more lenient parser for better performance
        soup = BeautifulSoup(html_content, "html.parser")
        segments = []
        mapping = {
            "nodes": {},  # Map segment indices to node paths
            "attributes": {},  # Map segment indices to attribute locations
            "form_elements": {},  # Map segment indices to form elements
            "select_options": {},  # Map segment indices to select options
            "metadata": {
                "structure_hash": self._generate_structure_hash(soup),
                "total_nodes": len(list(soup.descendants)),
                "html_hierarchy": self._generate_html_hierarchy(soup),
            },
        }
        segment_index = 0

        # First handle select elements specially
        segment_index = self._handle_select_options(soup, segments, mapping, segment_index)

        # Then handle other form elements
        segment_index = self._handle_form_elements(soup, segments, mapping, segment_index)

        # Then extract translatable attributes
        segment_index = self._extract_translatable_attributes(
            soup, segments, mapping, segment_index
        )

        # Then extract text content with better structure preservation
        segment_index = self._extract_translatable_text_nodes(
            soup, segments, mapping, segment_index
        )

        return segments, mapping

    def _generate_html_hierarchy(self, soup: BeautifulSoup) -> Dict:
        """
        Generate a simplified representation of the HTML hierarchy for structure validation

        Args:
            soup: BeautifulSoup document

        Returns:
            Dictionary representing the document structure
        """

        def extract_structure(element):
            if isinstance(element, NavigableString):
                return None

            result = {
                "tag": element.name,
                "attrs": {
                    k: v for k, v in element.attrs.items() if k in ["id", "class", "type", "name"]
                },
            }

            children = [
                extract_structure(c) for c in element.children if not isinstance(c, NavigableString)
            ]
            children = [c for c in children if c]  # Remove None values

            if children:
                result["children"] = children

            return result

        return extract_structure(soup)

    def _generate_structure_hash(self, soup: BeautifulSoup) -> str:
        """
        Generate a hash representing the document structure for verification

        Args:
            soup: BeautifulSoup document

        Returns:
            Hash string representing document structure
        """
        # Create a string representing the structure (tags and their hierarchy)
        structure = []
        for tag in soup.find_all():
            structure.append(f"{tag.name}:{tag.attrs.get('id', '')}:{tag.attrs.get('class', '')}")

        structure_str = "|".join(structure)
        return hashlib.md5(structure_str.encode()).hexdigest()[:10]

    # Add methods for extracting translatable content
    def _extract_translatable_attributes(self, soup, segments, mapping, start_index):
        # Implementation from the original file
        # ...
        index = start_index
        attr_mapping = {}

        # Optimize by getting all tags at once
        all_tags = soup.find_all()

        # Find all tags with translatable attributes
        for tag_index, tag in enumerate(all_tags):
            for attr in self.processor.TRANSLATABLE_ATTRS:
                if attr in tag.attrs and tag.attrs[attr].strip():
                    # Skip translation for URLs and file paths
                    if self._should_skip_attribute_translation(attr, tag.attrs[attr]):
                        continue

                    # Add attribute text to segments
                    segments.append(tag.attrs[attr])

                    # Store mapping with tag selector for more precise targeting
                    selector = self._get_css_selector(tag)
                    if selector not in attr_mapping:
                        attr_mapping[selector] = {}
                    attr_mapping[selector][attr] = index

                    # Also store in the main mapping
                    mapping["attributes"][index] = {
                        "selector": selector,
                        "attribute": attr,
                        "tag_index": tag_index,
                    }
                    index += 1

        return index

    # Add additional helper methods from HTMLProcessor
    def _should_skip_attribute_translation(self, attr_name, attr_value):
        """Determine if an attribute should be skipped for translation"""
        # Implementation from the original file
        # ...
        # Skip URLs
        if attr_name == "href" or attr_name == "src":
            # Check if it's a URL or file path
            if attr_value.startswith(("http", "https", "/", "./", "../")) or attr_value.endswith(
                (".html", ".htm", ".php", ".aspx", ".jsp")
            ):
                return True

        # Skip data attributes that might contain non-translatable information
        if attr_name.startswith("data-"):
            return True

        # Skip IDs, classes, and similar attributes
        if attr_name in ["id", "class", "name", "rel"]:
            return True

        return False

    def _get_css_selector(self, tag):
        """Generate a CSS selector that can uniquely identify this tag"""
        # Implementation from the original file
        # ...
        parts = []
        current = tag

        while current and current.name != "[document]":
            # Start with tag name
            selector = current.name

            # Add ID if available
            if current.has_attr("id"):
                selector += f"#{current['id']}"
                # ID should be unique, so we can stop here
                parts.insert(0, selector)
                break

            # Add classes
            if current.has_attr("class"):
                selector += "." + ".".join(current["class"])

            # Add position among siblings
            parent = current.parent
            siblings = list(parent.find_all(current.name, recursive=False)) if parent else []
            if len(siblings) > 1:
                position = siblings.index(current) + 1
                selector += f":nth-of-type({position})"

            parts.insert(0, selector)
            current = current.parent

        return " > ".join(parts)

    def _extract_translatable_text_nodes(self, soup, segments, mapping, start_index):
        """Extract text nodes that should be translated while preserving structure"""
        # Implementation from the original file
        # ...
        index = start_index

        # Process each translatable tag
        for tag_name in self.processor.TRANSLATABLE_TAGS:
            for tag in soup.find_all(tag_name):
                # Skip if tag is nested in IGNORE_TAGS or empty
                if self._is_in_ignore_tag(tag) or not tag.get_text().strip():
                    continue

                # Skip if this is a select or option - they're handled separately
                if tag.name in ["select", "option"]:
                    continue

                # Process this tag's contents, handling complex nested structures
                processed_nodes = []
                self._process_mixed_content(tag, processed_nodes)

                # Only handle tags with actual text content
                has_text = any(isinstance(node, str) and node.strip() for node in processed_nodes)
                if not has_text:
                    continue

                # Create a segment with placeholders for inline elements
                composite_text, node_map = self._create_composite_text(processed_nodes)
                if composite_text.strip():
                    segments.append(composite_text)
                    # Store mapping with more complete information
                    selector = self._get_css_selector(tag)
                    mapping["nodes"][index] = {
                        "selector": selector,
                        "node_map": node_map,
                        "tag": tag.name,
                        "original": composite_text,
                    }
                    index += 1

        return index

    def _is_in_ignore_tag(self, tag):
        """Check if tag is within an ignored tag"""
        # Implementation from the original file
        # ...
        parent = tag.parent
        while parent:
            if parent.name in self.processor.IGNORE_TAGS:
                return True
            parent = parent.parent
        return False

    def _process_mixed_content(self, tag, result):
        """Process mixed content (text and elements) within a tag"""
        # Implementation from the original file
        # ...
        for child in tag.children:
            if isinstance(child, NavigableString):
                text = str(child).strip()
                if text:  # Only add non-empty strings
                    result.append(str(child))  # Preserve exact string including whitespace
            elif child.name in self.processor.PRESERVED_INLINE_TAGS:
                # For inline formatting tags, handle them specially
                inner_content = []
                self._process_mixed_content(child, inner_content)
                if inner_content:  # Only add if it has content
                    result.append(
                        {"tag": child.name, "content": inner_content, "attrs": dict(child.attrs)}
                    )
            elif child.name not in self.processor.IGNORE_TAGS:
                # Recursively process other elements
                self._process_mixed_content(child, result)

    def _create_composite_text(self, nodes):
        """Create composite text with placeholders for inline elements"""
        # Implementation from the original file
        # ...
        result = []
        node_map = {}
        counter = 0

        for node in nodes:
            if isinstance(node, str):
                result.append(node)
            else:
                # It's an element node, create a placeholder
                placeholder = f"[TAG:{counter}]"
                result.append(placeholder)
                node_map[counter] = node
                counter += 1

        return "".join(result), node_map

    def _handle_form_elements(self, soup, segments, mapping, start_index):
        """Process form elements with special attention to their needs"""
        # Implementation from the original file
        # ...
        index = start_index

        # Handle select elements and their options
        for select_tag in soup.find_all("select"):
            # Skip if in ignore tag
            if self._is_in_ignore_tag(select_tag):
                continue

            select_selector = self._get_css_selector(select_tag)

            # Process each option
            for option in select_tag.find_all("option"):
                option_text = option.get_text().strip()
                if option_text:
                    segments.append(option_text)

                    # Store mapping for this option
                    mapping["form_elements"] = mapping.get("form_elements", {})
                    mapping["form_elements"][index] = {
                        "type": "option",
                        "selector": self._get_css_selector(option),
                        "parent_selector": select_selector,
                        "original": option_text,
                        "attributes": {k: v for k, v in option.attrs.items()},
                    }
                    index += 1

        # Handle buttons with text content
        for button in soup.find_all("button"):
            # Skip if in ignore tag or empty
            if self._is_in_ignore_tag(button) or not button.get_text().strip():
                continue

            button_text = button.get_text().strip()
            segments.append(button_text)

            # Store mapping for this button
            mapping["form_elements"] = mapping.get("form_elements", {})
            mapping["form_elements"][index] = {
                "type": "button",
                "selector": self._get_css_selector(button),
                "original": button_text,
            }
            index += 1

        # Handle input elements with translatable attributes
        for input_tag in soup.find_all("input"):
            # Skip if in ignore tag
            if self._is_in_ignore_tag(input_tag):
                continue

            # Translatable input attributes
            for attr in ["placeholder", "value", "alt", "title"]:
                if attr in input_tag.attrs and input_tag.attrs[attr].strip():
                    # Skip if it's a submit/button value that doesn't need translation
                    if attr == "value" and input_tag.get("type", "") in [
                        "hidden",
                        "file",
                        "image",
                        "reset",
                    ]:
                        continue

                    attr_value = input_tag.attrs[attr]
                    segments.append(attr_value)

                    # Store mapping for this attribute
                    mapping["form_elements"] = mapping.get("form_elements", {})
                    mapping["form_elements"][index] = {
                        "type": "input_attr",
                        "selector": self._get_css_selector(input_tag),
                        "attribute": attr,
                        "original": attr_value,
                    }
                    index += 1

        return index

    def _handle_select_options(self, soup, segments, mapping, start_index):
        """Process select elements and their options carefully to preserve structure"""
        # Implementation from the original file
        # ...
        index = start_index

        # Find all select elements
        for select_tag in soup.find_all("select"):
            # Skip if in ignore tag
            if self._is_in_ignore_tag(select_tag):
                continue

            select_selector = self._get_css_selector(select_tag)
            select_id = select_tag.get("id", "")
            select_class = " ".join(select_tag.get("class", []))

            # Store metadata about this select element
            mapping.setdefault("select_elements", {})
            select_info = {
                "selector": select_selector,
                "id": select_id,
                "class": select_class,
                "options": [],
            }

            # Process each option - IMPORTANT: Use direct find_all to preserve order
            options = select_tag.find_all("option", recursive=False)
            for option_idx, option in enumerate(options):
                # Use direct string extraction to avoid nested content issues
                # Get the exact string content to preserve whitespace
                option_text = "".join(str(content) for content in option.contents)

                # Skip if truly empty (not just whitespace)
                if not option_text and not option.string:
                    continue

                # Extract all attributes of the option
                option_attrs = {k: v for k, v in option.attrs.items()}

                # Store complete information about this option
                option_info = {
                    "index": option_idx,
                    "segment_index": index,
                    "attributes": option_attrs,
                    "original_text": option_text,
                    "selector": self._get_css_selector(option),
                }
                select_info["options"].append(option_info)

                # Add text to segments for translation (ensure we keep some whitespace)
                segments.append(option_text)

                # Also store in mapping for direct reference
                mapping["select_options"] = mapping.get("select_options", {})
                mapping["select_options"][index] = {
                    "select_selector": select_selector,
                    "option_selector": self._get_css_selector(option),
                    "option_index": option_idx,
                    "attributes": option_attrs,
                    "original_text": option_text,
                    "is_option": True,  # Mark explicitly as an option
                }

                index += 1

            # Store the complete select information
            select_key = f"select_{len(mapping['select_elements'])}"
            mapping["select_elements"][select_key] = select_info

        return index
