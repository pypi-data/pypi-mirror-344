"""Configuration validation for TransPhrase"""

import logging
from typing import Optional

from transphrase.core.config import TranslationConfig

logger = logging.getLogger("translator")


class ConfigurationValidator:
    """Handles validation of translation configuration"""

    REQUIRED_ATTRIBUTES = [
        "source_language",
        "target_language",
        "mode",
        "model",
        "system_prompt",
        "source_dir",
        "output_dir",
    ]

    @classmethod
    def validate_config(cls, config: Optional[TranslationConfig]) -> bool:
        """
        Validate the translation configuration

        Args:
            config: Configuration to validate

        Returns:
            bool: True if config is valid, False otherwise
        """
        if config is None:
            logger.error("Configuration cannot be None")
            return False

        if not isinstance(config, TranslationConfig):
            logger.error(f"Invalid configuration type: {type(config)}")
            return False

        # Check for missing or None attributes
        invalid_attrs = [
            attr
            for attr in cls.REQUIRED_ATTRIBUTES
            if not hasattr(config, attr) or getattr(config, attr) is None
        ]

        if invalid_attrs:
            logger.error(f"Missing or None required configuration attributes: {invalid_attrs}")
            return False

        # Validate specific attribute values
        if not config.source_dir or not config.output_dir:
            logger.error("Source and output directories must be specified")
            return False

        if not config.model:
            logger.error("Model must be specified")
            return False

        if config.mode not in ["translate", "polish"]:
            logger.error(f"Invalid mode: {config.mode}")
            return False

        return True

    @classmethod
    def get_safe_config_values(cls, config: TranslationConfig) -> dict:
        """
        Get safe default values for configuration attributes

        Args:
            config: Configuration object

        Returns:
            dict: Dictionary of safe configuration values
        """
        return {
            "source_language": getattr(config, "source_language", "auto-detected"),
            "target_language": getattr(config, "target_language", "English"),
            "mode": getattr(config, "mode", "translate"),
            "model": getattr(config, "model", "gpt-4"),
            "system_prompt": getattr(config, "system_prompt", ""),
            "source_dir": getattr(config, "source_dir", ""),
            "output_dir": getattr(config, "output_dir", ""),
        }
