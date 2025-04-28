"""Configuration management for TransPhrase"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from transphrase.rate_limiting.rate_limiter import RateLimitConfig

# Constants
MAX_CHUNK_SIZE = 4000  # Characters
MAX_RETRIES = 3
DEFAULT_MODEL = "deepseek-llm-67b-chat"
DEFAULT_WORKERS = 1
PAGE_SIZE = 15

# Supported languages
SUPPORTED_LANGUAGES = [
    "English",
    "Chinese",
    "Japanese",
    "Korean",
    "Spanish",
    "French",
    "German",
    "Russian",
    "Italian",
    "Portuguese",
    "Dutch",
    "Arabic",
    "Hindi",
]


@dataclass
class TranslationConfig:
    """Configuration for translation operations"""

    api_key: str
    model: str
    system_prompt: str
    workers: int
    skip_existing: bool
    source_dir: Path
    output_dir: Path
    source_language: str = "Chinese"
    target_language: str = "English"
    base_url: str = "https://api.electronhub.top"
    use_cache: bool = True
    cache_ttl: int = 86400  # 24 hours
    plugin_dirs: List[str] = field(default_factory=list)
    rate_limit_config: RateLimitConfig = field(default_factory=RateLimitConfig)
    db_path: str = "~/.transphrase/transphrase.db"


# Dynamic prompt template for translation
TRANSLATION_PROMPT_TEMPLATE = """
Translate the provided {source_language} text into high-quality {target_language}.
Ensure the translation is accurate, natural, consistent, and contains no {source_language} characters.

# Steps
1. Accuracy: Translate each chapter while faithfully conveying the original meaning, tone, style, and subtle details.
2. Naturalness: Ensure the {target_language} reads smoothly and naturally, maintaining grammatical correctness and idiomatic expressions.
3. Consistency: Pay particular attention to character names and ensure consistency throughout the translation to prevent errors.

# Output Format
The translated text should be in {target_language} only, devoid of any {source_language} characters.
Format the text to enhance readability.

# Notes
- Ensure the output text reaches the maximum length allowed by the model if possible.
- Use simple, clear formatting to facilitate ease of reading.
"""

# Maintain backward compatibility
DEFAULT_TRANSLATION_PROMPT = TRANSLATION_PROMPT_TEMPLATE.format(
    source_language="Chinese", target_language="English"
)

# Default polish prompt remains unchanged
DEFAULT_POLISH_PROMPT = """
You are an expert editor specializing in Honkai Impact 3rd fanfiction translations. Your task is to polish this machine-translated (MTL) chapter into fluent, emotionally immersive, and lore-accurate English while preserving the original plot, character voices, and key details.

Core Instructions:

1. Grammar & Flow:
   - Fix awkward phrasing, tense errors, and unnatural syntax.
   - Break up repetitive or run-on sentences for better pacing, especially in fights or emotional scenes.

2. Character Authenticity:
   - Match dialogue and inner monologues to personalities:
     - Kiana: Energetic, stubborn, with occasional humor.
     - Mei: Gentle, empathetic, but firm in crises.
     - Bronya: Emotionally reserved, blunt, with technical vocabulary.
   - Use official terms: 'Battlesuit,' 'Herrscher,' 'Stigmata,' 'Valkyries.'

3. Tone & Nuance:
   - Intensify emotional beats (angst, triumph, tension) without melodrama.
   - Replace nonsensical idioms with Honkai-appropriate equivalents.
   - Retain humor or sarcasm if contextually appropriate.

4. Clarity & Immersion:
   - Reword confusing MTL passages using Honkai lore.
   - Add subtle sensory details to enhance descriptions.

5. Don'ts:
   - Do not alter plot points, relationships, or lore.
   - Avoid slang or modern idioms unless used by characters like Tesla.

Example Edits:
Original: 'Bronya robot hand open fire. Mei cry, 'Please stop fight!''
Revised: 'Bronya's mechanical arm whirred as its cannon charged. Mei's plea cut through the chaos, 'Stop this! There's another way!''

Original: 'Seele heart hurt because Bronya not smile.'
Revised: 'Seele's chest tightened as she studied Bronya's impassive face—when did she last see her smile?'

Format: Retain symbols like [System Alert] if used.
"""
