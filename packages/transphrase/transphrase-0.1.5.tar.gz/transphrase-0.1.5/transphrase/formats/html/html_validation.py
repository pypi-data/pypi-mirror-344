"""HTML structure validation and repair"""

import re
from typing import Tuple

from bs4 import BeautifulSoup


class StructureValidator:
    """Validates and fixes HTML structure"""

    def validate_structure(self, original_html: str, translated_html: str) -> Tuple[bool, str]:
        """
        Validate that the translated HTML maintains proper structure

        Args:
            original_html: Original HTML content
            translated_html: Translated HTML content

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Parse both documents
        orig_soup = BeautifulSoup(original_html, "html.parser")
        trans_soup = BeautifulSoup(translated_html, "html.parser")

        # Check critical structural elements
        for tag in ["html", "head", "body"]:
            if orig_soup.find(tag) and not trans_soup.find(tag):
                return False, f"Missing {tag} tag in translated document"

        # Check for select/option integrity
        orig_selects = orig_soup.find_all("select")
        trans_selects = trans_soup.find_all("select")

        if len(orig_selects) != len(trans_selects):
            return False, f"Select count mismatch: {len(orig_selects)} vs {len(trans_selects)}"

        # Check each select element has its options
        for i, (orig_select, trans_select) in enumerate(zip(orig_selects, trans_selects)):
            orig_options = orig_select.find_all("option")
            trans_options = trans_select.find_all("option")

            if len(orig_options) != len(trans_options):
                return (
                    False,
                    f"Option count mismatch in select #{i+1}: {len(orig_options)} vs {len(trans_options)}",
                )

        return True, "HTML structure is valid"

    def fix_critical_issues(self, html_content: str, original_html: str = None) -> str:
        """
        Fix critical HTML structure issues, focusing on select/option elements

        Args:
            html_content: HTML content with issues
            original_html: Original HTML for reference

        Returns:
            Fixed HTML content
        """
        # Focus on common issues with select/option elements
        soup = BeautifulSoup(html_content, "html.parser")

        # 1. Find orphaned option text (text between option tags)
        for select in soup.find_all("select"):
            # Get direct string children of select that aren't whitespace
            for string in select.strings:
                if string.strip() and string.parent == select:
                    # This is text directly inside select - should be inside an option
                    # Find or create an option to contain it
                    new_option = soup.new_tag("option")
                    string.replace_with(new_option)
                    new_option.string = string

        # 2. Find broken option tags (option tags directly in body)
        for option in soup.find_all("option"):
            if option.parent and option.parent.name != "select":
                # This option is not inside a select - find nearest select
                nearest_select = soup.find("select")
                if nearest_select:
                    # Move this option inside the select
                    option.extract()
                    nearest_select.append(option)
                else:
                    # No select found, remove the orphaned option
                    option.decompose()

        # 3. Ensure all selects are properly closed
        html_str = str(soup)

        # Find select tags without proper closing
        select_pattern = re.compile(r"<select[^>]*>(?:(?!</select>).)*$", re.DOTALL)
        matches = select_pattern.findall(html_str)

        if matches:
            # Add missing closing tags
            for match in matches:
                html_str = html_str.replace(match, match + "</select>")

        # 4. Fix malformed options
        option_pattern = re.compile(r"(<option[^>]*>)(.*?)(</option>)", re.DOTALL)
        html_str = option_pattern.sub(r"\1\2\3", html_str)

        # 5. Clean up any text between options in selects
        select_cleanup = re.compile(r"(</option>)([^<]*?)(<option)", re.DOTALL)
        html_str = select_cleanup.sub(r"\1\3", html_str)

        # Final parsing to ensure well-formed HTML
        return str(BeautifulSoup(html_str, "html.parser"))
