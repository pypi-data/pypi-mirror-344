"""Handlers for API interactions"""

import logging
import time
from typing import List, Optional, TypedDict, Union

from openai import APIError, OpenAI, RateLimitError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from transphrase.cache.translation_cache import TranslationCache
from transphrase.core.config import MAX_RETRIES
from transphrase.rate_limiting.rate_limiter import AdaptiveRateLimiter

logger = logging.getLogger("translator")


class ModelInfo(TypedDict):
    """Type definition for model information"""

    id: str
    description: str
    tokens: Union[int, str]
    pricing: str
    capabilities: str


class APIHandler:
    """Handles API interactions for model listing and translation"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.electronhub.top",
        cache: Optional[TranslationCache] = None,
        rate_limiter: Optional[AdaptiveRateLimiter] = None,
    ):
        """
        Initialize API handler with credentials

        Args:
            api_key: OpenAI API key
            base_url: Base URL for API calls
            cache: Translation cache instance
            rate_limiter: Rate limiter instance
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.cache = cache
        self.rate_limiter = rate_limiter

    def fetch_available_models(self) -> List[ModelInfo]:
        """
        Fetch available models from the API with their descriptions and metadata

        Returns:
            List of model information dictionaries
        """
        try:
            response = self.client.models.list()
            models_info: List[ModelInfo] = []

            for model in response.data:
                model_id = model.id
                model_dict = model.model_dump() if hasattr(model, "model_dump") else vars(model)

                description = model_dict.get("description", "No description available")
                tokens = model_dict.get("tokens", "N/A")

                # Extract pricing information
                pricing = model_dict.get("pricing", {})
                price_input = pricing.get("input", "N/A") if isinstance(pricing, dict) else "N/A"
                price_output = pricing.get("output", "N/A") if isinstance(pricing, dict) else "N/A"

                # Extract capabilities from metadata
                metadata = model_dict.get("metadata", {})
                capabilities: List[str] = []
                if isinstance(metadata, dict):
                    if metadata.get("vision"):
                        capabilities.append("Vision")
                    if metadata.get("function_call"):
                        capabilities.append("Function call")
                    if metadata.get("web_search"):
                        capabilities.append("Web search")
                    if metadata.get("reasoning"):
                        capabilities.append("Reasoning")

                pricing_str = (
                    f"In: ${price_input} | Out: ${price_output}" if price_input != "N/A" else "N/A"
                )

                models_info.append(
                    {
                        "id": model_id,
                        "description": description,
                        "tokens": tokens,
                        "pricing": pricing_str,
                        "capabilities": ", ".join(capabilities) if capabilities else "N/A",
                    }
                )

            return sorted(models_info, key=lambda x: x["id"])
        except Exception as e:
            logger.error(f"Failed to fetch models: {e}")
            return []

    @retry(
        reraise=True,
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((APIError, RateLimitError, ConnectionError)),
    )
    def translate_chunk(
        self, system_prompt: str, text: str, model: str, series_id: Optional[str] = None
    ) -> str:
        """
        Translate a chunk of text using the specified model with glossary enhancement

        Args:
            system_prompt: System prompt to guide the translation
            text: Text to translate
            model: Model ID to use for translation
            series_id: Optional series ID for glossary terms

        Returns:
            Translated text with glossary terms applied
        """
        # Check cache first if available
        if self.cache:
            cached_translation = self.cache.get(text, system_prompt, model)
            if cached_translation:
                logger.info("Using cached translation")
                return cached_translation

        # Enhance prompt with glossary terms
        enhanced_prompt = self._enhance_prompt_with_glossary(system_prompt, series_id)

        # Apply rate limiting if configured
        if self.rate_limiter:
            wait_time = self.rate_limiter.before_request(
                model, len(text) // 4
            )  # Rough token estimate
            if wait_time > 0:
                logger.info(f"Rate limited, waiting {wait_time:.2f} seconds")
                time.sleep(wait_time)

        messages = [
            {"role": "system", "content": enhanced_prompt},
            {"role": "user", "content": text},
        ]

        try:
            resp = self.client.chat.completions.create(model=model, messages=messages, stream=False)

            translation = resp.choices[0].message.content

            # Update rate limiter with response headers
            if self.rate_limiter and hasattr(resp, "headers"):
                self.rate_limiter.after_response(
                    model, resp.headers, status_code=200
                )  # Explicit success status

            # Apply glossary terms to result before returning
            if self.cache and hasattr(self.cache, "apply_glossary_terms"):
                translation = self.cache.apply_glossary_terms(translation, series_id)

            # Cache the translation
            if self.cache:
                self.cache.set(text, system_prompt, model, translation)

            return translation

        except RateLimitError as e:
            # Extract wait time from error message if possible
            wait_time = 120  # Default to 2 minutes if we can't parse it
            try:
                error_msg = str(e)
                import re

                match = re.search(r"Try again in (\d+) seconds", error_msg)
                if match:
                    wait_time = int(match.group(1)) + 5  # Add buffer
                    logger.warning(
                        f"API requested wait of {match.group(1)} seconds, waiting {wait_time}"
                    )
            except Exception as parse_error:
                logger.warning(f"Failed to parse rate limit message: {parse_error}")

            # Update rate limiter with 429 status and parsed wait time
            if self.rate_limiter:
                # Set global rate limit to pause all requests
                if hasattr(self.rate_limiter, "set_global_rate_limit"):
                    self.rate_limiter.set_global_rate_limit(wait_time)

                # Rest of the code remains the same...

            # Let tenacity retry after the wait
            raise

    def _enhance_prompt_with_glossary(
        self, system_prompt: str, series_id: Optional[str] = None
    ) -> str:
        """Add glossary terms to the system prompt"""
        if not self.cache or not series_id:
            return system_prompt

        glossary = self.cache.get_cached_glossary(series_id)
        if not glossary:
            return system_prompt

        # Group terms by category
        categorized_terms = {}
        for source, info in glossary.items():
            category = info.get("category", "general")
            if category not in categorized_terms:
                categorized_terms[category] = []

            categorized_terms[category].append((source, info["target"]))

        # Build glossary section
        glossary_text = (
            "\n\n# SERIES GLOSSARY\nUse these exact translations for the following terms:\n"
        )

        # Add general terms first
        if "general" in categorized_terms:
            for source, target in categorized_terms["general"]:
                glossary_text += f'- "{source}" → "{target}"\n'

        # Add categorized terms
        for category, terms in categorized_terms.items():
            if category == "general":
                continue

            glossary_text += f"\n## {category.title()}\n"
            for source, target in terms:
                glossary_text += f'- "{source}" → "{target}"\n'

        return system_prompt + glossary_text
