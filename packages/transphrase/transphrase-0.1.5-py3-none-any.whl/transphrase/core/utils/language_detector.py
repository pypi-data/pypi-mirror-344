"""Language detection functionality for translation processing"""

import logging
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup, Tag
from langdetect import LangDetectException, detect

logger = logging.getLogger("translator")


class LanguageDetector:
    """Handles language detection operations"""

    # Language code mapping from ISO 639-1 to human-readable names
    LANGUAGE_CODES = {
        "en": "English",
        "zh": "Chinese",
        "ja": "Japanese",
        "ko": "Korean",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ru": "Russian",
        "pt": "Portuguese",
        "it": "Italian",
        "ar": "Arabic",
        "hi": "Hindi",
        "vi": "Vietnamese",
        "th": "Thai",
        "id": "Indonesian",
    }

    # Script systems to language mappings
    SCRIPT_TO_LANGUAGE = {
        "Latin": [
            "English",
            "Spanish",
            "French",
            "German",
            "Portuguese",
            "Italian",
            "Vietnamese",
            "Indonesian",
        ],
        "Cyrillic": ["Russian"],
        "CJK": ["Chinese", "Japanese", "Korean"],
        "Hiragana": ["Japanese"],
        "Katakana": ["Japanese"],
        "Hangul": ["Korean"],
        "Arabic": ["Arabic"],
        "Devanagari": ["Hindi"],
        "Thai": ["Thai"],
    }

    # Unicode character ranges for different scripts
    UNICODE_SCRIPTS = {
        "Latin": [
            (0x0020, 0x007F),  # Basic Latin
            (0x00A0, 0x00FF),  # Latin-1 Supplement
            (0x0100, 0x017F),  # Latin Extended-A
            (0x0180, 0x024F),  # Latin Extended-B
        ],
        "Cyrillic": [
            (0x0400, 0x04FF),  # Cyrillic
            (0x0500, 0x052F),  # Cyrillic Supplement
        ],
        "Hiragana": [(0x3040, 0x309F)],
        "Katakana": [(0x30A0, 0x30FF)],
        "CJK": [
            (0x4E00, 0x9FFF),  # CJK Unified Ideographs
            (0x3400, 0x4DBF),  # CJK Unified Ideographs Extension A
            (0x20000, 0x2A6DF),  # CJK Unified Ideographs Extension B
            (0x2A700, 0x2B73F),  # CJK Unified Ideographs Extension C
            (0x2B740, 0x2B81F),  # CJK Unified Ideographs Extension D
            (0x2B820, 0x2CEAF),  # CJK Unified Ideographs Extension E
            (0xF900, 0xFAFF),  # CJK Compatibility Ideographs
            (0x3300, 0x33FF),  # CJK Compatibility
            (0xFE30, 0xFE4F),  # CJK Compatibility Forms
        ],
        "Hangul": [
            (0xAC00, 0xD7AF),  # Hangul Syllables
            (0x1100, 0x11FF),  # Hangul Jamo
            (0x3130, 0x318F),  # Hangul Compatibility Jamo
        ],
        "Arabic": [(0x0600, 0x06FF)],
        "Devanagari": [(0x0900, 0x097F)],
        "Thai": [(0x0E00, 0x0E7F)],
    }

    def is_html_content(self, text: str) -> bool:
        """
        Check if the given text contains HTML content.

        Args:
            text: Text to check for HTML content

        Returns:
            True if HTML content is detected, False otherwise
        """
        # More robust HTML detection with regex
        html_pattern = re.compile(
            r"<(?:!DOCTYPE|html|head|body|div|p|h[1-6]|span|a|img|table|form|ul|ol)\b[^>]*>",
            re.IGNORECASE,
        )
        if html_pattern.search(text):
            return True

        # Check for common HTML entities
        html_entity_pattern = re.compile(r"&[a-z]+;|&#\d+;")
        if html_entity_pattern.search(text):
            return True

        return False

    def _extract_text_from_html(self, html: str) -> Tuple[str, Optional[str]]:
        """
        Extract text content from HTML with improved handling.

        Args:
            html: HTML content to parse

        Returns:
            Tuple of (extracted_text, lang_hint) where lang_hint is from HTML attributes
        """
        try:
            soup = BeautifulSoup(html, "html.parser")

            # Remove script and style elements that don't contain useful text
            for element in soup.select("script, style, meta, link"):
                element.extract()

            # Check for language hints in HTML or body tag
            lang_hint = None
            html_tag = soup.find("html")
            if html_tag and html_tag.get("lang"):
                lang_attr = html_tag.get("lang").lower()
                lang_code = lang_attr.split("-")[0] if "-" in lang_attr else lang_attr
                lang_hint = self.LANGUAGE_CODES.get(lang_code, lang_code)
                logger.debug(f"Found language hint in HTML: {lang_hint}")

            # Extract paragraphs and headings as they contain most meaningful content
            content_tags = soup.select("p, h1, h2, h3, h4, h5, h6, div > text")
            if content_tags:
                # Join content-rich tags with newlines to preserve structure
                extracted_text = "\n".join(
                    tag.get_text(strip=True) for tag in content_tags if tag.get_text(strip=True)
                )
                if extracted_text:
                    logger.debug(f"Extracted {len(extracted_text)} chars from content-rich tags")
                    return extracted_text, lang_hint

            # Fallback to extracting all text
            all_text = soup.get_text(separator="\n", strip=True)
            logger.debug(f"Used fallback text extraction, got {len(all_text)} chars")
            return all_text, lang_hint

        except Exception as e:
            logger.warning(f"Error extracting text from HTML: {e}")
            return html, None

    def _detect_script_type(self, text: str) -> Dict[str, float]:
        """
        Detect the dominant script system in the text based on character analysis.

        Args:
            text: The text to analyze

        Returns:
            Dictionary mapping script names to their percentage of the text
        """
        if not text:
            return {}

        char_count = len(text)
        script_counts = Counter()

        # Count characters by script
        for char in text:
            # Skip whitespace and punctuation
            if char.isspace() or unicodedata.category(char).startswith("P"):
                char_count -= 1
                continue

            # Check which script the character belongs to
            char_script = self._get_char_script(char)
            if char_script:
                script_counts[char_script] += 1

        # Calculate percentages
        if char_count > 0:
            script_percentages = {
                script: count / char_count for script, count in script_counts.items()
            }
            logger.debug(f"Script analysis: {dict(script_percentages)}")
            return script_percentages

        return {}

    def _get_char_script(self, char: str) -> Optional[str]:
        """
        Determine which script a character belongs to.

        Args:
            char: Single character to check

        Returns:
            Script name or None if not matched
        """
        code_point = ord(char)

        for script, ranges in self.UNICODE_SCRIPTS.items():
            for start, end in ranges:
                if start <= code_point <= end:
                    return script

        return None

    def _get_language_from_script(self, script_percentages: Dict[str, float]) -> Optional[str]:
        """
        Determine the most likely language based on script analysis.

        Args:
            script_percentages: Dictionary of script percentages

        Returns:
            Most likely language or None if undetermined
        """
        if not script_percentages:
            return None

        # Get the dominant script
        dominant_script, percentage = max(script_percentages.items(), key=lambda x: x[1])

        # If the dominant script has high confidence (>50%), use it
        if percentage > 0.5:
            logger.debug(f"Dominant script is {dominant_script} ({percentage:.2%})")

            # For scripts that map directly to a single language
            if dominant_script in ["Hiragana", "Katakana"]:
                return "Japanese"
            elif dominant_script == "Hangul":
                return "Korean"
            elif dominant_script == "Devanagari":
                return "Hindi"
            elif dominant_script == "Thai":
                return "Thai"
            elif dominant_script == "Arabic":
                return "Arabic"

            # For CJK scripts, we need to distinguish between Chinese, Japanese, and Korean
            elif dominant_script == "CJK":
                # Check for presence of Japanese or Korean specific scripts
                has_japanese_scripts = (
                    "Hiragana" in script_percentages or "Katakana" in script_percentages
                )
                has_korean_scripts = "Hangul" in script_percentages

                if has_japanese_scripts:
                    return "Japanese"
                elif has_korean_scripts:
                    return "Korean"
                else:
                    # If only CJK characters and no Japanese or Korean specific scripts, likely Chinese
                    return "Chinese"

            # For Latin script, we need statistical analysis (handled by langdetect)
            # For Cyrillic, if it's dominant, it's likely Russian
            elif dominant_script == "Cyrillic":
                return "Russian"

        return None

    def detect_language(self, text: str, min_length: int = 100) -> Optional[str]:
        """
        Detect the language of the given text.

        Args:
            text: Text to analyze (can be plain text or HTML)
            min_length: Minimum text length for reliable detection

        Returns:
            Language name or None if detection fails
        """
        if not text:
            logger.debug("Empty text provided for language detection")
            return None

        # Check if content is HTML
        html_content = self.is_html_content(text)

        # Extract text from HTML if needed
        lang_hint = None
        if html_content:
            text, lang_hint = self._extract_text_from_html(text)
            logger.debug(f"Processed HTML content, extracted {len(text)} chars of text")

            # If we have a language hint from HTML and the content is short, we might trust the hint
            if lang_hint and len(text) < min_length:
                logger.debug(f"Using language hint from HTML: {lang_hint}")
                return lang_hint

        # Perform script analysis for additional language hints
        script_percentages = self._detect_script_type(text)
        script_based_language = self._get_language_from_script(script_percentages)

        # If we got a high confidence script-based language detection, use it
        if script_based_language:
            logger.debug(f"Detected language from script analysis: {script_based_language}")
            return script_based_language

        # If text is too short, detection may be unreliable
        if len(text) < min_length:
            logger.debug(f"Text too short for reliable language detection: {len(text)} chars")
            return None

        try:
            # For very long texts, sample a portion to speed up detection
            if len(text) > 10000:
                # Sample beginning, middle, and end
                sample_size = min(3000, len(text) // 3)
                beginning = text[:sample_size]
                middle_start = max(0, (len(text) - sample_size) // 2)
                middle = text[middle_start : middle_start + sample_size]
                end = text[-sample_size:] if len(text) > sample_size else ""

                text_sample = beginning + " " + middle + " " + end
                logger.debug(f"Sampling long text: {len(text)} chars → {len(text_sample)} chars")
                text = text_sample

            lang_code = detect(text)
            detected_lang = self.LANGUAGE_CODES.get(lang_code, lang_code)

            # If we have a hint that conflicts with detection, log it
            if lang_hint and lang_hint != detected_lang:
                logger.debug(
                    f"HTML language hint ({lang_hint}) differs from detected language ({detected_lang})"
                )

            # If script analysis conflicts with statistical detection, use the more reliable script analysis
            if script_based_language and script_based_language != detected_lang:
                # For certain scripts that are highly reliable indicators, prefer script analysis
                reliable_scripts = ["Hiragana", "Katakana", "Hangul", "Thai", "Devanagari", "CJK"]

                # For CJK content, give higher priority to script-based detection for Chinese
                if script_based_language == "Chinese" and "CJK" in script_percentages:
                    cjk_percentage = script_percentages.get("CJK", 0)
                    if cjk_percentage > 0.7:  # If text is predominantly CJK characters
                        logger.debug(
                            f"Preferring Chinese detection based on high CJK content ({cjk_percentage:.1%})"
                        )
                        return "Chinese"

                # For other reliable scripts, prefer script analysis over statistical
                if any(
                    script in script_percentages and script_percentages[script] > 0.3
                    for script in reliable_scripts
                ):
                    logger.debug(
                        f"Preferring script-based detection ({script_based_language}) over statistical detection ({detected_lang})"
                    )
                    return script_based_language

            logger.debug(f"Detected language: {detected_lang}")
            return detected_lang

        except LangDetectException as e:
            logger.warning(f"Language detection failed: {e}")
            # If detection fails, try using script analysis or HTML hint as fallback
            if script_based_language:
                logger.debug(f"Using script analysis as fallback: {script_based_language}")
                return script_based_language
            if lang_hint:
                logger.debug(f"Using language hint as fallback: {lang_hint}")
                return lang_hint
            return None

    def detect_files_language(
        self, files: List[Path], sample_size: int = 5, text_sample_bytes: int = 3000
    ) -> Optional[str]:
        """
        Detect the dominant language across multiple files.

        Args:
            files: List of files to sample
            sample_size: Number of files to sample
            text_sample_bytes: Number of bytes to read from each file

        Returns:
            Detected language name or None if detection fails
        """
        if not files:
            return None

        # Sample a subset of files
        sample_files = files[: min(sample_size, len(files))]
        detected_languages = []

        for file_path in sample_files:
            try:
                # Read a portion of the file
                text = file_path.read_text(encoding="utf-8", errors="ignore")
                sample_text = text[:text_sample_bytes]

                lang = self.detect_language(sample_text)
                if lang:
                    detected_languages.append(lang)
                    logger.debug(f"Detected {lang} in {file_path.name}")
            except Exception as e:
                logger.error(f"Error reading file {file_path} for language detection: {e}")

        # Use most common detected language
        if detected_languages:
            most_common_lang = Counter(detected_languages).most_common(1)[0][0]
            logger.info(f"Auto-detected source language: {most_common_lang}")
            return most_common_lang

        return None
