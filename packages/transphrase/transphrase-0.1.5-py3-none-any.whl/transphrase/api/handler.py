"""Handlers for API interactions.

This module provides the APIHandler class which manages all interactions with
the translation API, including model listing, translation requests, and
rate limiting.
"""

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
    """Type definition for model information.

    Attributes:
        id: Unique model identifier
        description: Human-readable description of the model
        tokens: Maximum token capacity or token information
        pricing: Pricing information for input/output tokens
        capabilities: List of model capabilities
    """

    id: str
    description: str
    tokens: Union[int, str]
    pricing: str
    capabilities: str


class APIHandler:
    """Handles API interactions for model listing and translation.

    This class manages all communication with the translation API, including:
    - Listing available models and their capabilities
    - Handling translation requests with rate limiting
    - Caching translations for improved performance
    - Managing API credentials and configuration

    Attributes:
        client: OpenAI client instance
        cache: Translation cache instance
        rate_limiter: Rate limiter instance
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.electronhub.top",
        cache: Optional[TranslationCache] = None,
        rate_limiter: Optional[AdaptiveRateLimiter] = None,
    ):
        """Initialize API handler with credentials.

        Args:
            api_key: OpenAI API key (required)
            base_url: Base URL for API calls (default: "https://api.electronhub.top")
            cache: Translation cache instance (optional)
            rate_limiter: Rate limiter instance (optional)

        Raises:
            ValueError: If api_key is empty or invalid
        """
        if not api_key:
            raise ValueError("API key cannot be empty")

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
        """Translate a chunk of text using the specified model with glossary enhancement.

        This method handles the entire translation process including:
        - Checking the cache for existing translations
        - Enhancing the prompt with glossary terms
        - Applying rate limiting
        - Making the API request
        - Applying glossary terms to the result
        - Caching the translation

        Args:
            system_prompt: System prompt to guide the translation (required)
            text: Text to translate (required)
            model: Model ID to use for translation (required)
            series_id: Optional series ID for glossary terms

        Returns:
            str: Translated text with glossary terms applied

        Raises:
            ValueError: If any required parameter is empty
            APIError: If the API request fails
            RateLimitError: If rate limits are exceeded
        """
        if not system_prompt or not text or not model:
            raise ValueError("system_prompt, text, and model parameters cannot be empty")

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

            # Let tenacity retry after the wait
            raise

    def translate_batch(
        self, system_prompt: str, texts: List[str], model: str, series_id: Optional[str] = None
    ) -> List[str]:
        """Translate multiple text chunks in a single API call for better performance.

        Args:
            system_prompt: System prompt to guide the translation
            texts: List of text chunks to translate
            model: Model ID to use for translation
            series_id: Optional series ID for glossary terms

        Returns:
            List of translated texts in the same order

        Raises:
            ValueError: If any required parameter is empty
            APIError: If the API request fails
        """
        if not system_prompt or not texts or not model:
            raise ValueError("system_prompt, texts, and model parameters cannot be empty")

        if not texts:
            return []

        # If only one text, use the regular translate_chunk method
        if len(texts) == 1:
            return [self.translate_chunk(system_prompt, texts[0], model, series_id)]

        # Check cache for all texts
        translations = [None] * len(texts)
        uncached_indices = []

        if self.cache:
            for i, text in enumerate(texts):
                cached = self.cache.get(text, system_prompt, model)
                if cached:
                    translations[i] = cached
                else:
                    uncached_indices.append(i)
        else:
            uncached_indices = list(range(len(texts)))

        # If all texts were in cache, return immediately
        if not uncached_indices:
            return translations

        # Construct a single prompt with all uncached texts
        uncached_texts = [texts[i] for i in uncached_indices]

        # Enhance prompt with glossary terms
        enhanced_prompt = self._enhance_prompt_with_glossary(system_prompt, series_id)

        # Apply rate limiting if configured
        if self.rate_limiter:
            total_tokens = sum(len(text) // 4 for text in uncached_texts)  # Rough token estimate
            wait_time = self.rate_limiter.before_request(model, total_tokens)
            if wait_time > 0:
                logger.info(f"Rate limited, waiting {wait_time:.2f} seconds")
                time.sleep(wait_time)

        # Use a stable, deterministic delimiter instead of hash
        # Create a unique delimiter with a fixed prefix and a timestamp-based suffix
        import uuid

        stable_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, "transphrase.delimiter"))[:8]
        delimiter = f"[CHUNK_DELIMITER_{stable_id}]"

        # Join all texts with the delimiter
        batch_text = delimiter.join(uncached_texts)

        # Create a special system prompt that instructs to preserve the delimiters
        batch_prompt = (
            f"{enhanced_prompt}\n\n"
            f"IMPORTANT: The input contains multiple separate texts divided by the delimiter: {delimiter}\n"
            f"Translate each section independently, maintaining the original sections separated by the exact same delimiter."
        )

        messages = [
            {"role": "system", "content": batch_prompt},
            {"role": "user", "content": batch_text},
        ]

        try:
            resp = self.client.chat.completions.create(model=model, messages=messages, stream=False)
            result = resp.choices[0].message.content

            # Update rate limiter with response headers
            if self.rate_limiter and hasattr(resp, "headers"):
                self.rate_limiter.after_response(model, resp.headers, status_code=200)

            # Split the result by delimiter
            result_parts = result.split(delimiter)

            # Handle case where API didn't maintain the delimiter structure
            if len(result_parts) != len(uncached_texts):
                logger.warning(
                    f"Batch translation returned {len(result_parts)} parts instead of {len(uncached_texts)}"
                )
                # Fall back to individual translations
                for i, idx in enumerate(uncached_indices):
                    translations[idx] = self.translate_chunk(
                        system_prompt, texts[idx], model, series_id
                    )
            else:
                # Apply glossary terms and cache each part
                for i, idx in enumerate(uncached_indices):
                    part = result_parts[i]

                    if self.cache and hasattr(self.cache, "apply_glossary_terms"):
                        part = self.cache.apply_glossary_terms(part, series_id)

                    # Cache the translation
                    if self.cache:
                        self.cache.set(texts[idx], system_prompt, model, part)

                    translations[idx] = part

            return translations

        except Exception as e:
            logger.error(f"Batch translation failed: {str(e)}")
            # Fall back to individual translations
            for i, idx in enumerate(uncached_indices):
                try:
                    translations[idx] = self.translate_chunk(
                        system_prompt, texts[idx], model, series_id
                    )
                except Exception as inner_e:
                    logger.error(f"Individual translation failed: {str(inner_e)}")
                    translations[idx] = texts[idx]  # Fall back to original text

            return translations

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
