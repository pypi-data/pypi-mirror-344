"""Series-level context management for maintaining consistency across multiple documents."""

import json
import logging
import sqlite3
import time  # Add this import
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("translator")


class SeriesContext:
    """Manages context across a series of related documents."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize the series context manager.

        Args:
            cache_dir: Directory for storing context data (defaults to ~/.transphrase/cache)
        """
        self.cache_dir = cache_dir or Path("~/.transphrase/cache").expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize DB
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the SQLite database for series context storage."""
        db_path = self.cache_dir / "series_context.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Create tables if they don't exist
        # Series table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS series (
                series_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_at INTEGER,
                updated_at INTEGER
            )
            """
        )

        # Character names table with relationships
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS characters (
                series_id TEXT,
                name TEXT,
                description TEXT,
                aliases TEXT,  -- JSON list of alternative names
                relationships TEXT,  -- JSON object of related characters
                first_appearance TEXT,  -- File where first seen
                PRIMARY KEY (series_id, name),
                FOREIGN KEY (series_id) REFERENCES series(series_id)
            )
            """
        )

        # Terminology table for consistent terms
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS terminology (
                series_id TEXT,
                source_term TEXT,
                target_term TEXT,
                description TEXT,
                category TEXT,
                priority INTEGER DEFAULT 1,  -- Higher priority terms take precedence
                PRIMARY KEY (series_id, source_term),
                FOREIGN KEY (series_id) REFERENCES series(series_id)
            )
            """
        )

        # Jobs associated with a series
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS series_jobs (
                series_id TEXT,
                job_id TEXT,
                UNIQUE(series_id, job_id),
                FOREIGN KEY (series_id) REFERENCES series(series_id)
            )
            """
        )

        conn.commit()
        conn.close()

    def create_series(self, name: str, description: str = "") -> str:
        """
        Create a new series for context tracking.

        Args:
            name: Name of the series
            description: Optional description

        Returns:
            Series ID
        """
        series_id = str(uuid.uuid4())
        current_time = int(time.time())

        conn = sqlite3.connect(str(self.cache_dir / "series_context.db"))
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO series VALUES (?, ?, ?, ?, ?)",
            (series_id, name, description, current_time, current_time),
        )

        conn.commit()
        conn.close()

        logger.info(f"Created new series '{name}' with ID {series_id}")
        return series_id

    def get_series_list(self) -> List[Dict[str, Any]]:
        """
        Get list of all series.

        Returns:
            List of series information dictionaries
        """
        conn = sqlite3.connect(str(self.cache_dir / "series_context.db"))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM series ORDER BY updated_at DESC")
        series_list = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return series_list

    def associate_job_with_series(self, job_id: str, series_id: str) -> None:
        """
        Associate a translation job with a series.

        Args:
            job_id: Translation job ID
            series_id: Series ID
        """
        conn = sqlite3.connect(str(self.cache_dir / "series_context.db"))
        cursor = conn.cursor()

        cursor.execute("INSERT OR IGNORE INTO series_jobs VALUES (?, ?)", (series_id, job_id))

        conn.commit()
        conn.close()

        logger.info(f"Associated job {job_id} with series {series_id}")

    def add_character(
        self,
        series_id: str,
        name: str,
        description: str = "",
        aliases: List[str] = None,
        relationships: Dict[str, str] = None,
        first_appearance: str = "",
    ) -> None:
        """
        Add or update a character in the series context.

        Args:
            series_id: Series ID
            name: Character name
            description: Character description
            aliases: Alternative names for the character
            relationships: Relationships to other characters (name -> relationship)
            first_appearance: File where character first appeared
        """
        aliases = aliases or []
        relationships = relationships or {}

        conn = sqlite3.connect(str(self.cache_dir / "series_context.db"))
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR REPLACE INTO characters VALUES (?, ?, ?, ?, ?, ?)",
            (
                series_id,
                name,
                description,
                json.dumps(aliases),
                json.dumps(relationships),
                first_appearance,
            ),
        )

        # Update series timestamp
        cursor.execute(
            "UPDATE series SET updated_at = ? WHERE series_id = ?", (int(time.time()), series_id)
        )

        conn.commit()
        conn.close()

        logger.info(f"Added/updated character '{name}' in series {series_id}")

    def add_terminology(
        self,
        series_id: str,
        source_term: str,
        target_term: str,
        description: str = "",
        category: str = "general",
        priority: int = 1,
    ) -> None:
        """
        Add or update terminology in the series context.

        Args:
            series_id: Series ID
            source_term: Term in source language
            target_term: Term in target language
            description: Description or context for the term
            category: Category for grouping terms (e.g., "magic", "locations")
            priority: Priority (higher numbers take precedence)
        """
        conn = sqlite3.connect(str(self.cache_dir / "series_context.db"))
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR REPLACE INTO terminology VALUES (?, ?, ?, ?, ?, ?)",
            (series_id, source_term, target_term, description, category, priority),
        )

        # Update series timestamp
        cursor.execute(
            "UPDATE series SET updated_at = ? WHERE series_id = ?", (int(time.time()), series_id)
        )

        conn.commit()
        conn.close()

        logger.info(f"Added/updated term '{source_term}' → '{target_term}' in series {series_id}")

    def get_characters(self, series_id: str) -> List[Dict[str, Any]]:
        """
        Get all characters for a series.

        Args:
            series_id: Series ID

        Returns:
            List of character dictionaries
        """
        conn = sqlite3.connect(str(self.cache_dir / "series_context.db"))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM characters WHERE series_id = ?", (series_id,))
        characters = []

        for row in cursor.fetchall():
            char_dict = dict(row)
            # Parse JSON fields
            char_dict["aliases"] = json.loads(char_dict["aliases"])
            char_dict["relationships"] = json.loads(char_dict["relationships"])
            characters.append(char_dict)

        conn.close()
        return characters

    def get_terminology(
        self, series_id: str, category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get terminology for a series, optionally filtered by category.

        Args:
            series_id: Series ID
            category: Optional category filter

        Returns:
            List of terminology dictionaries
        """
        conn = sqlite3.connect(str(self.cache_dir / "series_context.db"))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if category:
            cursor.execute(
                "SELECT * FROM terminology WHERE series_id = ? AND category = ? ORDER BY priority DESC",
                (series_id, category),
            )
        else:
            cursor.execute(
                "SELECT * FROM terminology WHERE series_id = ? ORDER BY priority DESC", (series_id,)
            )

        terminology = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return terminology

    def generate_context_prompt(self, series_id: str, chunk_text: str) -> str:
        """
        Generate context enhancement for a prompt based on series data.

        Args:
            series_id: Series ID
            chunk_text: Current chunk being translated

        Returns:
            Context addition for the prompt
        """
        characters = self.get_characters(series_id)
        terminology = self.get_terminology(series_id)

        # Filter to only include relevant characters and terms
        relevant_characters = []
        relevant_terms = []

        # Simple relevance check - if name/term appears in chunk
        for char in characters:
            if char["name"] in chunk_text:
                relevant_characters.append(char)
                continue

            # Check aliases too
            for alias in char["aliases"]:
                if alias in chunk_text:
                    relevant_characters.append(char)
                    break

        for term in terminology:
            if term["source_term"] in chunk_text:
                relevant_terms.append(term)

        # Build context prompt
        context_parts = []

        if relevant_characters:
            char_section = "## Important Characters\n"
            for char in relevant_characters[:5]:  # Limit to 5 most relevant characters
                aliases_str = (
                    f" (also known as: {', '.join(char['aliases'])})" if char["aliases"] else ""
                )
                char_section += f"- {char['name']}{aliases_str}: {char['description']}\n"
            context_parts.append(char_section)

        if relevant_terms:
            term_section = "## Key Terminology\n"
            for term in relevant_terms[:10]:  # Limit to 10 most important terms
                term_section += (
                    f"- '{term['source_term']}' should be translated as '{term['target_term']}'\n"
                )
            context_parts.append(term_section)

        if not context_parts:
            return ""

        return "\n".join(
            [
                "# SERIES CONTEXT - USE THIS INFORMATION FOR CONSISTENCY",
                *context_parts,
                "Maintain consistency with the above character names and terminology.\n",
            ]
        )
