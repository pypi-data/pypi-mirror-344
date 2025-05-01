"""Unit tests for ConfigurationValidator"""

import unittest
from unittest.mock import Mock

from transphrase.core.config import TranslationConfig
from transphrase.core.config_validator import ConfigurationValidator


class TestConfigurationValidator(unittest.TestCase):
    def setUp(self):
        self.valid_config = TranslationConfig(
            source_language="en",
            target_language="es",
            mode="translate",
            model="gpt-4",
            system_prompt="Translate this text",
            source_dir="/input",
            output_dir="/output",
            api_key="test-key",
            workers=4,
            skip_existing=False,
        )

    def test_validate_valid_config(self):
        self.assertTrue(ConfigurationValidator.validate_config(self.valid_config))

    def test_validate_none_config(self):
        self.assertFalse(ConfigurationValidator.validate_config(None))

    def test_validate_invalid_type(self):
        self.assertFalse(ConfigurationValidator.validate_config("invalid"))

    def test_validate_missing_attributes(self):
        # Create a valid config then remove attributes
        config = TranslationConfig(
            source_language="en",
            target_language="es",
            mode="translate",
            model="gpt-4",
            system_prompt="Translate this text",
            source_dir="/input",
            output_dir="/output",
            api_key="test-key",
            workers=4,
            skip_existing=False,
        )
        # Set required attributes to None
        config.source_language = None
        config.target_language = None
        self.assertFalse(ConfigurationValidator.validate_config(config))

    def test_get_safe_values(self):
        # Create config with only some attributes
        partial_config = TranslationConfig(
            source_language="en",
            target_language="es",
            mode="translate",
            model="gpt-4",
            system_prompt="Translate this text",
            source_dir="/input",
            output_dir="/output",
            api_key="test-key",
            workers=4,
            skip_existing=False,
        )
        safe_values = ConfigurationValidator.get_safe_config_values(partial_config)

        self.assertEqual(safe_values["source_language"], "en")
        self.assertEqual(safe_values["target_language"], "es")
        self.assertEqual(safe_values["mode"], "translate")
        self.assertEqual(safe_values["model"], "gpt-4")
        self.assertEqual(safe_values["system_prompt"], "Translate this text")
        self.assertEqual(safe_values["source_dir"], "/input")
        self.assertEqual(safe_values["output_dir"], "/output")

    def test_validate_invalid_mode(self):
        invalid_config = TranslationConfig(
            source_language="en",
            target_language="es",
            mode="invalid",
            model="gpt-4",
            system_prompt="Translate this text",
            source_dir="/input",
            output_dir="/output",
            api_key="test-key",
            workers=4,
            skip_existing=False,
        )
        self.assertFalse(ConfigurationValidator.validate_config(invalid_config))


if __name__ == "__main__":
    unittest.main()
