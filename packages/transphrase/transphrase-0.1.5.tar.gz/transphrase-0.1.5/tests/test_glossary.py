import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from transphrase.cache.series_context import SeriesContext
from transphrase.cache.translation_cache import TranslationCache


class TestGlossaryFeatures(unittest.TestCase):

    def setUp(self):
        # Set up test environment
        self.cache = TranslationCache(cache_dir="/tmp/transphrase_test")
        self.series_context = SeriesContext(db_path=":memory:")

        # Create test series
        self.series_id = self.series_context.create_series("Test Series", "Test Description")

        # Add some test terminology
        self.series_context.add_terminology(
            self.series_id, "灵气", "Spiritual Energy", category="cultivation", priority=5
        )
        self.series_context.add_terminology(
            self.series_id,
            "张三",
            "Zhang San",
            category="character",
            priority=10,
            case_sensitive=True,
        )

    def test_load_glossary(self):
        """Test loading glossary from series context"""
        with patch.object(SeriesContext, "get_terminology") as mock_get:
            mock_get.return_value = [
                {
                    "source_term": "灵气",
                    "target_term": "Spiritual Energy",
                    "category": "cultivation",
                    "priority": 5,
                    "case_sensitive": False,
                },
                {
                    "source_term": "张三",
                    "target_term": "Zhang San",
                    "category": "character",
                    "priority": 10,
                    "case_sensitive": True,
                },
            ]

            glossary = self.cache.load_series_glossary(self.series_id)

            self.assertEqual(len(glossary), 2)
            self.assertEqual(glossary["灵气"]["target"], "Spiritual Energy")
            self.assertEqual(glossary["张三"]["category"], "character")

    def test_apply_glossary_terms(self):
        """Test applying glossary terms to text"""
        with patch.object(TranslationCache, "get_cached_glossary") as mock_get:
            mock_get.return_value = {
                "灵气": {"target": "Spiritual Energy", "case_sensitive": False},
                "张三": {"target": "Zhang San", "case_sensitive": True},
            }

            # Test case-insensitive replacement
            text = "他感受到了灵气的存在，灵气充满了整个空间。"
            expected = "他感受到了Spiritual Energy的存在，Spiritual Energy充满了整个空间。"
            self.assertEqual(self.cache.apply_glossary_terms(text, self.series_id), expected)

            # Test case-sensitive replacement
            text = "张三和张三的朋友来了。"
            expected = "Zhang San和Zhang San的朋友来了。"
            self.assertEqual(self.cache.apply_glossary_terms(text, self.series_id), expected)

    def tearDown(self):
        # Clean up
        import shutil

        shutil.rmtree("/tmp/transphrase_test", ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
