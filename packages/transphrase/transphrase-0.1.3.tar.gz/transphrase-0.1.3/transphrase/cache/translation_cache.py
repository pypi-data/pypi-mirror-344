import hashlib
import json
import os
import re
import sqlite3
import time
from pathlib import Path
from typing import Dict, Optional


class TranslationCache:
    """Cache for translation API responses to reduce duplicate calls"""

    def __init__(self, cache_dir: str = "~/.transphrase/cache", ttl: int = 86400):
        """
        Initialize the translation cache

        Args:
            cache_dir: Directory to store cache files
            ttl: Time-to-live in seconds for cache entries (default: 24 hours)
        """
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl

        # Initialize SQLite database for cache
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the SQLite database for cache storage"""
        db_path = self.cache_dir / "translation_cache.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Create cache table if it doesn't exist
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS translation_cache (
            key TEXT PRIMARY KEY,
            model TEXT,
            response TEXT,
            timestamp INTEGER
        )
        """
        )

        # Add glossary_terms table to translation cache
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS glossary_terms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                series_id TEXT,
                source_term TEXT,
                target_term TEXT,
                category TEXT,
                priority INTEGER DEFAULT 1,
                case_sensitive BOOLEAN DEFAULT 0,
                timestamp INTEGER,
                UNIQUE(series_id, source_term)
            )
            """
        )

        conn.commit()
        conn.close()

    def _get_key(self, text: str, system_prompt: str, model: str) -> str:
        """Generate a unique key for the cache entry"""
        data = f"{text}|{system_prompt}|{model}"
        return hashlib.md5(data.encode()).hexdigest()

    def get(self, text: str, system_prompt: str, model: str) -> Optional[str]:
        """
        Get a cached translation if available

        Args:
            text: Text to be translated
            system_prompt: System prompt used for translation
            model: Model ID used for translation

        Returns:
            Cached translation or None if not found or expired
        """
        key = self._get_key(text, system_prompt, model)
        db_path = self.cache_dir / "translation_cache.db"

        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            cursor.execute(
                "SELECT response, timestamp FROM translation_cache WHERE key = ? AND model = ?",
                (key, model),
            )
            result = cursor.fetchone()
            conn.close()

            if result:
                response, timestamp = result
                # Check if cache entry is still valid
                if time.time() - timestamp <= self.ttl:
                    return response

            return None
        except Exception as e:
            print(f"Cache error: {e}")
            return None

    def set(self, text: str, system_prompt: str, model: str, translation: str) -> None:
        """
        Store a translation in the cache

        Args:
            text: Original text
            system_prompt: System prompt used for translation
            model: Model ID used for translation
            translation: Translated text to cache
        """
        key = self._get_key(text, system_prompt, model)
        db_path = self.cache_dir / "translation_cache.db"

        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            cursor.execute(
                "INSERT OR REPLACE INTO translation_cache VALUES (?, ?, ?, ?)",
                (key, model, translation, int(time.time())),
            )

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Cache error: {e}")

    def load_series_glossary(self, series_id: str) -> Dict[str, Dict]:
        """Load glossary terms for a specific series"""
        if not series_id:
            return {}

        db_path = self.cache_dir / "translation_cache.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Get terminology from series database
        from transphrase.cache.series_context import SeriesContext

        series_context = SeriesContext()
        terms = series_context.get_terminology(series_id)

        # Store terms in local cache for efficient lookup during translation
        for term in terms:
            cursor.execute(
                """
                INSERT OR REPLACE INTO glossary_terms
                (series_id, source_term, target_term, category, priority, case_sensitive, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    series_id,
                    term["source_term"],
                    term["target_term"],
                    term.get("category", "general"),
                    term.get("priority", 1),
                    term.get("case_sensitive", False),
                    int(time.time()),
                ),
            )

        conn.commit()
        conn.close()

        return self.get_cached_glossary(series_id)

    def get_cached_glossary(self, series_id: Optional[str] = None) -> Dict[str, Dict]:
        """Get glossary terms from cache"""
        db_path = self.cache_dir / "translation_cache.db"
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        glossary = {}

        # Query terms, sorted by length (longest first) and priority
        if series_id:
            cursor.execute(
                """
                SELECT source_term, target_term, category, priority, case_sensitive
                FROM glossary_terms
                WHERE series_id = ?
                ORDER BY LENGTH(source_term) DESC, priority DESC
                """,
                (series_id,),
            )
        else:
            cursor.execute(
                """
                SELECT source_term, target_term, category, priority, case_sensitive
                FROM glossary_terms
                ORDER BY LENGTH(source_term) DESC, priority DESC
                """
            )

        for row in cursor.fetchall():
            source, target, category, priority, case_sensitive = row
            glossary[source] = {
                "target": target,
                "category": category,
                "priority": priority,
                "case_sensitive": bool(case_sensitive),
            }

        conn.close()
        return glossary

    def apply_glossary_terms(self, text: str, series_id: Optional[str] = None) -> str:
        """Apply glossary terms to translated text for consistency"""
        glossary = self.get_cached_glossary(series_id)
        if not glossary:
            return text

        result = text

        # Apply terms in order (longest first, highest priority first)
        for source_term, info in glossary.items():
            target_term = info["target"]
            case_sensitive = info.get("case_sensitive", False)

            if case_sensitive:
                # Simple case-sensitive replacement
                result = result.replace(source_term, target_term)
            else:
                # Case-insensitive replacement using regex
                pattern = re.compile(re.escape(source_term), re.IGNORECASE)
                result = pattern.sub(target_term, result)

        return result
