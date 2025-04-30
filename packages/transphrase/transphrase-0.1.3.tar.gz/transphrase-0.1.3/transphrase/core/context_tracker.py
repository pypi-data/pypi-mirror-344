"""Context tracking for maintaining translation quality across files."""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Set

from transphrase.cache.context_cache import ContextCache
from transphrase.cache.series_context import SeriesContext

logger = logging.getLogger("translator")


class ContextTracker:
    """Tracks and maintains context across multiple translation files."""

    def __init__(
        self,
        job_id: str,
        source_language: str,
        target_language: str,
        model: str,
        series_id: Optional[str] = None,
    ):
        """
        Initialize context tracker for a translation job

        Args:
            job_id: Unique job identifier
            source_language: Source language of translation
            target_language: Target language of translation
            model: Model being used for translation
            series_id: Optional ID of the series this job belongs to
        """
        self.job_id = job_id
        self.source_language = source_language
        self.target_language = target_language
        self.model = model
        self.series_id = series_id

        # Track current file
        self.current_file: Optional[Path] = None
        self.file_chunk_counter: Dict[str, int] = {}

        # Track name frequencies to only add after threshold is reached
        self.name_frequencies: Dict[str, int] = {}
        self.name_frequency_threshold = 10  # Only add names that appear at least 10 times

        # Initialize context cache
        self.context_cache = ContextCache()
        self.context_cache.start_job(job_id, source_language, target_language, model)

        # Initialize series context if provided
        self.series_context = None
        if series_id:
            self.series_context = SeriesContext()
            # Associate this job with the series
            self.series_context.associate_job_with_series(job_id, series_id)
            logger.info(f"Job {job_id} associated with series {series_id}")

    def start_file(self, file_path: Path) -> None:
        """
        Set the current active file for context tracking.

        Args:
            file_path: Path to the file being processed
        """
        self.current_file = file_path
        self.file_chunk_counter[str(file_path)] = 0
        logger.info(f"Starting context tracking for file: {file_path}")

    def update_context(self, source_text: str, translation: str) -> None:
        """Update context with new translated chunk."""
        if not self.current_file:
            logger.warning("Cannot update context: No active file")
            return

        file_path = str(self.current_file)
        chunk_index = self.file_chunk_counter[file_path]

        # Update context in cache
        self.context_cache.update_context(source_text, translation, file_path, chunk_index)

        # Update series context with new characters and terms if needed
        if self.series_context and self.series_id:
            # Extract potential new character names
            new_names = self.context_cache.extractor.extract_names(
                translation, language=self.target_language
            )

            # Get existing characters to check if any are new
            existing_characters = {
                char["name"] for char in self.series_context.get_characters(self.series_id)
            }

            # Update frequency counter for all detected names
            for name in new_names:
                if len(name) > 1:
                    self.name_frequencies[name] = self.name_frequencies.get(name, 0) + 1

                    # Only add new characters that exceed the frequency threshold
                    if (
                        name not in existing_characters
                        and self.name_frequencies[name] >= self.name_frequency_threshold
                    ):
                        # Add with minimal info, can be enriched later
                        self.series_context.add_character(
                            self.series_id,
                            name,
                            description=f"Auto-detected character (frequency: {self.name_frequencies[name]})",
                            first_appearance=file_path,
                        )
                        logger.info(
                            f"Auto-added character '{name}' with frequency {self.name_frequencies[name]}"
                        )

        # Increment chunk counter
        self.file_chunk_counter[file_path] += 1

    def get_enhanced_prompt(self, base_prompt: str, chunk_text: str) -> str:
        """
        Get system prompt enhanced with relevant context.

        Args:
            base_prompt: Base system prompt
            chunk_text: Current text chunk being translated

        Returns:
            Enhanced prompt with context
        """
        # Start with job-specific context from context cache
        enhanced_prompt = self.context_cache.get_enhanced_prompt(base_prompt, chunk_text)

        # Add series-wide context if available
        if self.series_context and self.series_id:
            series_context = self.series_context.generate_context_prompt(self.series_id, chunk_text)
            if series_context:
                # Insert series context after the base prompt but before job context
                parts = enhanced_prompt.split("# TRANSLATION CONTEXT")
                if len(parts) > 1:
                    enhanced_prompt = (
                        parts[0] + series_context + "\n# TRANSLATION CONTEXT" + parts[1]
                    )
                else:
                    enhanced_prompt += "\n\n" + series_context

        return enhanced_prompt

    def extract_glossary_from_context(self) -> Dict[str, List[Dict]]:
        """
        Extract a glossary from the current context for review or export.

        Returns:
            Dictionary with characters and terminology
        """
        # Get job-specific context from database
        job_context = self.context_cache.get_job_context(self.job_id)

        result = {"characters": [], "terminology": []}

        # Add characters with frequency
        for name, freq in job_context.get("names", {}).items():
            result["characters"].append(
                {"name": name, "frequency": freq, "description": "", "aliases": []}
            )

        # Add terminology with frequency
        for term, freq in job_context.get("terms", {}).items():
            result["terminology"].append(
                {
                    "source_term": term,
                    "target_term": term,  # Same by default, can be edited
                    "frequency": freq,
                    "description": "",
                    "category": "general",
                }
            )

        return result
