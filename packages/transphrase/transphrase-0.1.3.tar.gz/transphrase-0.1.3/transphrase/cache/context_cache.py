"""Context caching for maintaining translation consistency."""

import logging
import re
import sqlite3
import time
from pathlib import Path
from typing import Set

from transphrase.cache.language_constants import (
    COMMON_CHINESE_SURNAMES,
    COMMON_STARTERS,
    JAPANESE_HONORIFICS,
    KOREAN_SURNAMES,
)

logger = logging.getLogger("translator")


class ContextExtractor:
    """Extracts key context elements from text."""

    @staticmethod
    def extract_names(text: str, language: str = "English") -> Set[str]:
        """
        Extract potential character names from text.

        Args:
            text: Text to analyze
            language: Source language for language-specific extraction

        Returns:
            Set of potential character names
        """
        potential_names = set()

        # Language-specific extraction strategies
        if language == "English":
            # English extraction (capitalized words)
            common_starters = COMMON_STARTERS

            # Find capitalized words that aren't at sentence start
            words = re.findall(r"\b[A-Z][a-z]{2,}\b", text)

            # Filter out common starters at the beginning of sentences
            for word in words:
                if word not in common_starters:
                    potential_names.add(word)

            # Also look for quoted names like "Xiao Lan"
            quoted_names = re.findall(r'"([^"]*)"', text)
            for name in quoted_names:
                if len(name.split()) <= 3:  # Likely a name if 1-3 words
                    potential_names.add(name)

            # Look for repeated adjacent capitalized words (likely character names)
            repeated_caps = re.findall(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b", text)
            potential_names.update(repeated_caps)

        elif language == "Chinese":
            # For Chinese, look for repeated name patterns and names in quotes
            # Common family name characters (simplified)
            common_surnames = COMMON_CHINESE_SURNAMES

            # Find quotation marks that might contain names
            quoted_text = re.findall(r'["' '](.*?)["' "]", text)
            for qt in quoted_text:
                if 2 <= len(qt) <= 6:  # Chinese names are typically 2-3 characters
                    potential_names.add(qt)

            # Find patterns where surnames are followed by one or two characters
            for surname in common_surnames:
                pattern = surname + r"[\u4e00-\u9fff]{1,2}"
                matches = re.findall(pattern, text)
                potential_names.update(matches)

        elif language == "Japanese":
            # For Japanese, focus on patterns with honorifics
            honorifics = JAPANESE_HONORIFICS

            # Find names with honorifics
            for honorific in honorifics:
                pattern = r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]{1,5}" + honorific
                matches = re.findall(pattern, text)
                for match in matches:
                    # Remove the honorific to get just the name
                    name = match[: -len(honorific)]
                    potential_names.add(name)

            # Look for quoted names
            quoted_names = re.findall(r"「([^」]{1,10})」", text)
            for name in quoted_names:
                if 1 <= len(name) <= 5:  # Reasonable length for Japanese names
                    potential_names.add(name)

        elif language == "Korean":
            # For Korean, common family names and patterns
            # Common Korean surnames
            korean_surnames = KOREAN_SURNAMES

            # Find patterns with common surnames
            for surname in korean_surnames:
                pattern = surname + r"[가-힣]{1,3}"
                matches = re.findall(pattern, text)
                potential_names.update(matches)

            # Look for quoted names
            quoted_names = re.findall(r'"([^"]{1,10})"', text)
            for name in quoted_names:
                if 2 <= len(name) <= 6:  # Reasonable length for Korean names
                    potential_names.add(name)

        # Generic patterns for any language
        # Look for consistent capitalized patterns across multiple languages
        # This helps with transliterated names that might appear in any text

        # Add dialogue-based name extraction (before/after speech)
        dialogue_patterns = [
            r'"[^"]+?," ([A-Z][a-z]+) said\b',
            r'"[^"]+?," said ([A-Z][a-z]+)\b',
            r'([A-Z][a-z]+) said,? "[^"]+"',
            r'([A-Z][a-z]+) replied,? "[^"]+"',
            r'([A-Z][a-z]+) asked,? "[^"]+"',
            r'([A-Z][a-z]+) shouted,? "[^"]+"',
            r'([A-Z][a-z]+) whispered,? "[^"]+"',
        ]

        for pattern in dialogue_patterns:
            matches = re.findall(pattern, text)
            potential_names.update(matches)

        return potential_names

    @staticmethod
    def extract_terms(text: str, prev_terms: Set[str]) -> Set[str]:
        """Extract recurring domain-specific terms."""
        # Look for capitalized terms that appear multiple times
        all_terms = set()

        # Find potential special terms (capitalized or in quotes)
        special_terms = re.findall(r"\b[A-Z][a-zA-Z]+\b", text)

        # Add terms that also appeared in previous content
        for term in special_terms:
            if term in prev_terms or special_terms.count(term) > 1:
                all_terms.add(term)

        return all_terms

    @staticmethod
    def extract_summary(text: str, max_length: int = 500) -> str:
        """Create a concise summary of the text."""
        # Simple implementation: take first and last paragraph
        paragraphs = text.split("\n\n")

        if not paragraphs:
            return ""

        # Get first paragraph
        summary = paragraphs[0]

        # Add last paragraph if different from first
        if len(paragraphs) > 1 and paragraphs[-1] != paragraphs[0]:
            summary += "\n\n" + paragraphs[-1]

        # Truncate if too long
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."

        return summary


class ContextCache:
    """Cache for maintaining translation context across chunks and files."""

    def __init__(
        self, cache_dir: str = "~/.transphrase/context", ttl: int = 604800
    ):  # 1 week default
        """
        Initialize the context cache

        Args:
            cache_dir: Directory to store context cache
            ttl: Time-to-live in seconds for cache entries
        """
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl

        # Initialize SQLite database
        self._init_db()

        # In-memory context for current session
        self.current_context = {
            "names": set(),
            "terms": set(),
            "summaries": [],
            "job_id": None,
            "source_language": None,
            "target_language": None,
        }

        self.extractor = ContextExtractor()

    def _init_db(self) -> None:
        """Initialize the SQLite database for context storage."""
        db_path = self.cache_dir / "context_cache.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Create tables if they don't exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS context_jobs (
                job_id TEXT PRIMARY KEY,
                source_language TEXT,
                target_language TEXT,
                updated_at INTEGER,
                model TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS context_names (
                job_id TEXT,
                name TEXT,
                frequency INTEGER DEFAULT 1,
                UNIQUE(job_id, name)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS context_terms (
                job_id TEXT,
                term TEXT,
                frequency INTEGER DEFAULT 1,
                UNIQUE(job_id, term)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS context_summaries (
                job_id TEXT,
                file_path TEXT,
                summary TEXT,
                chunk_index INTEGER,
                UNIQUE(job_id, file_path, chunk_index)
            )
        """
        )

        conn.commit()
        conn.close()

    def start_job(
        self, job_id: str, source_language: str, target_language: str, model: str
    ) -> None:
        """Initialize or resume a translation job context."""
        # Reset in-memory context
        self.current_context = {
            "names": set(),
            "terms": set(),
            "summaries": [],
            "job_id": job_id,
            "source_language": source_language,
            "target_language": target_language,
        }

        # Check if job exists in database
        db_path = self.cache_dir / "context_cache.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Create or update job record
        cursor.execute(
            "INSERT OR REPLACE INTO context_jobs VALUES (?, ?, ?, ?, ?)",
            (job_id, source_language, target_language, int(time.time()), model),
        )

        # Load existing context for this job
        cursor.execute("SELECT name FROM context_names WHERE job_id = ?", (job_id,))
        for row in cursor.fetchall():
            self.current_context["names"].add(row[0])

        cursor.execute("SELECT term FROM context_terms WHERE job_id = ?", (job_id,))
        for row in cursor.fetchall():
            self.current_context["terms"].add(row[0])

        cursor.execute(
            "SELECT summary FROM context_summaries WHERE job_id = ? ORDER BY chunk_index", (job_id,)
        )
        for row in cursor.fetchall():
            if len(self.current_context["summaries"]) < 5:  # Limit to last 5 summaries
                self.current_context["summaries"].append(row[0])

        conn.commit()
        conn.close()

        logger.info(
            f"Loaded context for job {job_id}: {len(self.current_context['names'])} names, "
            f"{len(self.current_context['terms'])} terms, "
            f"{len(self.current_context['summaries'])} summaries"
        )

    def update_context(self, text: str, translation: str, file_path: str, chunk_index: int) -> None:
        """Update context based on a new processed chunk and its translation."""
        job_id = self.current_context["job_id"]
        if not job_id:
            logger.warning("Cannot update context: No active job")
            return

        # Extract context from translation (target language)
        new_names = self.extractor.extract_names(translation)
        new_terms = self.extractor.extract_terms(translation, self.current_context["terms"])
        summary = self.extractor.extract_summary(translation)

        # Update in-memory context
        self.current_context["names"].update(new_names)
        self.current_context["terms"].update(new_terms)

        # Keep only recent summaries (max 5)
        self.current_context["summaries"].append(summary)
        if len(self.current_context["summaries"]) > 5:
            self.current_context["summaries"] = self.current_context["summaries"][-5:]

        # Update database
        db_path = self.cache_dir / "context_cache.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Update names
        for name in new_names:
            cursor.execute("INSERT OR IGNORE INTO context_names VALUES (?, ?, 1)", (job_id, name))
            cursor.execute(
                "UPDATE context_names SET frequency = frequency + 1 WHERE job_id = ? AND name = ?",
                (job_id, name),
            )

        # Update terms
        for term in new_terms:
            cursor.execute("INSERT OR IGNORE INTO context_terms VALUES (?, ?, 1)", (job_id, term))
            cursor.execute(
                "UPDATE context_terms SET frequency = frequency + 1 WHERE job_id = ? AND term = ?",
                (job_id, term),
            )

        # Add summary
        cursor.execute(
            "INSERT OR REPLACE INTO context_summaries VALUES (?, ?, ?, ?)",
            (job_id, str(file_path), summary, chunk_index),
        )

        # Update job timestamp
        cursor.execute(
            "UPDATE context_jobs SET updated_at = ? WHERE job_id = ?", (int(time.time()), job_id)
        )

        conn.commit()
        conn.close()

    def get_enhanced_prompt(self, system_prompt: str, chunk_text: str) -> str:
        """Generate an enhanced prompt with context for the next chunk."""
        job_id = self.current_context["job_id"]
        if not job_id:
            return system_prompt

        # Get top names by frequency
        db_path = self.cache_dir / "context_cache.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM context_names WHERE job_id = ? ORDER BY frequency DESC LIMIT 15",
            (job_id,),
        )
        top_names = [row[0] for row in cursor.fetchall()]

        cursor.execute(
            "SELECT term FROM context_terms WHERE job_id = ? ORDER BY frequency DESC LIMIT 15",
            (job_id,),
        )
        top_terms = [row[0] for row in cursor.fetchall()]

        conn.close()

        # Create context section for prompt
        context_sections = []

        if top_names:
            context_sections.append(
                f"# Important Names\nConsistently use these character/place names: {', '.join(top_names)}"
            )

        if top_terms:
            context_sections.append(
                f"# Key Terms\nMaintain consistent terminology for: {', '.join(top_terms)}"
            )

        if self.current_context["summaries"]:
            context_sections.append(
                "# Previous Content\nBuild upon this context from previous text:"
            )
            # Add most recent 2 summaries
            for i, summary in enumerate(self.current_context["summaries"][-2:]):
                if summary.strip():
                    context_sections.append(f"Chunk {i+1}: {summary.strip()}")

        # Combine original prompt with context
        if context_sections:
            enhanced_prompt = (
                f"{system_prompt}\n\n# TRANSLATION CONTEXT\n{chr(10).join(context_sections)}"
            )
            return enhanced_prompt
        else:
            return system_prompt

    def clear_old_contexts(self) -> None:
        """Clear expired context data based on TTL."""
        current_time = int(time.time())
        expiration_time = current_time - self.ttl

        db_path = self.cache_dir / "context_cache.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Get expired jobs
        cursor.execute("SELECT job_id FROM context_jobs WHERE updated_at < ?", (expiration_time,))
        expired_jobs = [row[0] for row in cursor.fetchall()]

        for job_id in expired_jobs:
            # Delete all related records
            cursor.execute("DELETE FROM context_names WHERE job_id = ?", (job_id,))
            cursor.execute("DELETE FROM context_terms WHERE job_id = ?", (job_id,))
            cursor.execute("DELETE FROM context_summaries WHERE job_id = ?", (job_id,))
            cursor.execute("DELETE FROM context_jobs WHERE job_id = ?", (job_id,))

        conn.commit()
        conn.close()

        if expired_jobs:
            logger.info(f"Cleared {len(expired_jobs)} expired context caches")
