import hashlib
import json
import os
import sqlite3
import time
from pathlib import Path
from typing import Optional


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
