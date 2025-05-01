"""Configuration management for TransPhrase"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from transphrase.rate_limiting.rate_limiter import RateLimitConfig

# Constants
MAX_CHUNK_SIZE = 5500  # Characters
MAX_RETRIES = 3
DEFAULT_MODEL = "deepseek-llm-67b-chat"
DEFAULT_WORKERS = 1
PAGE_SIZE = 15


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
    mode: str = "translate"
    source_language: str = "Chinese"
    target_language: str = "English"
    polish_style: str = "standard"
    base_url: str = "https://api.electronhub.top"
    use_cache: bool = True
    use_context_cache: bool = True  # Enable context caching by default
    cache_ttl: int = 86400  # 24 hours
    context_cache_ttl: int = 604800  # 7 days
    plugin_dirs: List[str] = field(default_factory=list)
    rate_limit_config: RateLimitConfig = field(default_factory=RateLimitConfig)
    db_path: str = "~/.transphrase/transphrase.db"
    max_chunk_size: int = MAX_CHUNK_SIZE
    use_glossary: bool = True
    glossary_enforce: bool = True
    series_id: Optional[str] = None
    auto_detect_language: bool = True  # Enable by default for better user experience


# Dynamic prompt template for translation
TRANSLATION_PROMPT_TEMPLATE = """
You are an expert translator. Convert the given **{source_language}** text into polished, idiomatic **{target_language}** prose—preserving meaning, tone, style, and character voices.
---
**🔍 Step-by-Step Guide**
1. **Fidelity**
   - Render every nuance—literal meanings, implied subtext, emotional beats—without omission or addition.
2. **Fluency**
   - Write in natural, idiomatic **{target_language}**.
   - Vary sentence rhythm: short, punchy lines for action; longer, flowing sentences for reflection.
3. **Consistency**
   - Keep all names, terms, and stylistic markers uniform across the text.
   - Use a glossary if provided; otherwise, create a terminology list as you translate.
4. **Clarity & Readability**
   - Break up dense paragraphs.
   - Use simple HTML-like markers (e.g., line breaks, paragraphs) to improve flow.

---
**📋 Output Requirements**
- **Language**: Only **{target_language}**—zero **{source_language}** characters or words.
- **Formatting**:
  - Paragraphs separated by a blank line.
  - Dialogue on its own line, with proper quotation marks.
- **Length**: Aim to fully translate the input; maximize detail without padding.

---

**⚠️ Don't**
- Leave transliterations or untranslated source text.
- Inject personal commentary or footnotes.
- Alter plot, dialogue intent, or character personalities.

"""

# Maintain backward compatibility
DEFAULT_TRANSLATION_PROMPT = TRANSLATION_PROMPT_TEMPLATE.format(
    source_language="Chinese", target_language="English"
)

# Base polish prompt template
POLISH_PROMPT_TEMPLATE = """
You are an expert editor specializing in improving text quality. Your task is to transform this text into fluent, emotionally immersive, and accurate **{target_language}** while preserving the original meaning, character voices, and key details.

**1. Grammar & Flow**
- Eliminate awkward phrasing, tense errors, and unnatural syntax.
- Vary sentence length for pacing—short bursts in action scenes, longer beats in contemplative moments.
- Ensure the text follows natural **{target_language}** conventions and idioms.

**2. Character Authenticity**
- Match dialogue and inner monologues to each character's defined personality.
- Maintain consistent terminology for special terms, names, and concepts.
- Preserve the original tone and style of different speakers.

**3. Tone & Nuance**
- Heighten emotional beats without slipping into melodrama.
- Replace awkward expressions with natural **{target_language}** phrasing.
- Retain humor or sarcasm where contextually appropriate.

**4. Clarity & Immersion**
- Reword confusing passages to enhance clarity.
- Where appropriate, add subtle sensory details to ground the reader.
- Ensure transitions between scenes and thoughts flow naturally.

**5. Don'ts**
- Never change plot points, relationships, or core content.
- Avoid adding your own commentary or footnotes.
- Don't alter the fundamental meaning of any passage.

{style_guidance}

Format the text with proper paragraphs, dialogue formatting, and structure according to **{target_language}** conventions.
"""

# Language-specific polish templates
LANGUAGE_SPECIFIC_POLISH = {
    "English": """
Additional English-specific guidance:
- Use contractions where appropriate for natural speech (e.g., "I'm" vs "I am").
- Vary verb choices to avoid overuse of "went," "said," "was," etc.
- Employ active voice predominantly but use passive voice when appropriate for emphasis.
- Ensure proper handling of articles (a, an, the) and prepositions.
""",
    "Chinese": """
Additional Chinese-specific guidance:
- Ensure appropriate use of measure words (量词) with nouns.
- Maintain natural topic-comment structure rather than strict subject-verb-object patterns.
- Use appropriate 4-character expressions (成语) when they fit naturally.
- Ensure proper use of aspect markers (了, 过, 着) rather than relying on tense.
- Avoid excessive pronouns where context makes the subject clear.
""",
    "Japanese": """
Additional Japanese-specific guidance:
- Use appropriate levels of formality (敬語, 丁寧語, 常体) consistently.
- Ensure correct use of particles (は, が, を, に, etc.).
- Maintain proper sentence-final expressions that reflect the speaker's personality.
- Use appropriate gendered language and self-references based on character.
- Ensure natural SOV (Subject-Object-Verb) sentence structure.
""",
    "Korean": """
Additional Korean-specific guidance:
- Maintain appropriate honorific levels (존댓말 vs 반말) consistently.
- Ensure proper use of sentence-ending particles to convey nuance.
- Use appropriate level of formality based on relationships between characters.
- Maintain natural topic-comment structure with appropriate particles.
- Preserve culturally specific expressions and concepts.
""",
    "Spanish": """
Additional Spanish-specific guidance:
- Ensure proper use of subjunctive mood where appropriate.
- Maintain consistent use of formal (usted) vs informal (tú) address.
- Use appropriate regional expressions if the setting is specific.
- Ensure correct gendered agreement of adjectives and articles.
- Vary sentence structures to sound natural, using common Spanish connectors.
""",
    "French": """
Additional French-specific guidance:
- Maintain consistent use of formal (vous) vs informal (tu) address.
- Ensure proper use of subjunctive and conditional moods.
- Use elegant connecting phrases for a flowing, sophisticated style.
- Ensure correct gendered agreements and article usage.
- Preserve culturally specific expressions when appropriate.
""",
    "German": """
Additional German-specific guidance:
- Ensure proper case usage (nominative, accusative, dative, genitive).
- Maintain correct word order, especially in subordinate clauses.
- Use appropriate modal particles (doch, mal, ja, etc.) for nuance.
- Ensure proper noun gender assignments and corresponding article use.
- Preserve compound nouns where appropriate instead of breaking into phrases.
""",
}

# Writing style presets
POLISH_STYLE_PRESETS = {
    "standard": """
Style guidance: Maintain a balanced, natural writing style appropriate to the context.
""",
    "formal": """
Style guidance: Elevate the language to a more formal register while maintaining clarity.
- Use more complex sentence structures and elevated vocabulary.
- Minimize contractions and colloquialisms.
- Employ more precise terminology and formal transitions.
- Maintain a respectful, professional distance in narration.
- Use more sophisticated connectors and transitional phrases.
""",
    "creative": """
Style guidance: Enhance the artistic and expressive qualities of the writing.
- Employ rich, evocative imagery and sensory details.
- Use more poetic language, metaphors, and similes when appropriate.
- Vary rhythm and flow with greater contrast between sentences.
- Intensify emotional beats with more nuanced expression.
- Develop distinctive voice patterns for each character.
""",
    "technical": """
Style guidance: Optimize for clarity, precision, and information density.
- Prioritize clear, unambiguous phrasing over stylistic flourishes.
- Use more precise terminology and maintain consistent technical vocabulary.
- Structure information logically with clear cause-effect relationships.
- Break down complex concepts into digestible components.
- Use formatting conventions appropriate for technical content.
""",
    "conversational": """
Style guidance: Make the text flow like natural, engaging conversation.
- Use contractions, discourse markers, and casual connecting phrases.
- Incorporate rhetorical questions and conversational asides where appropriate.
- Vary between longer explanations and punchy, direct statements.
- Include occasional humor and personality in the narration.
- Ensure dialogue sounds like real people talking, not written speech.
""",
}

HTML_TRANSLATION_PROMPT_TEMPLATE = """
You are an expert HTML translator. Convert the given **{source_language}** text into polished, idiomatic **{target_language}** while PERFECTLY preserving ALL HTML structure, tags, and attributes.

**CRITICAL INSTRUCTIONS:**
1. Translate ONLY the visible text content that would appear in a browser
2. DO NOT modify ANY HTML tags or attributes - not even a single character
3. Keep all HTML entities (like &nbsp;) unchanged
4. NEVER separate option tags from their select container
5. NEVER move text outside of its original parent tags
6. NEVER add or remove any HTML tags or attributes
7. MUST keep ALL content inside the exact same tags it was in originally
8. NEVER translate content within <script>, <style>, or HTML comments
9. DO NOT wrap your response in markdown code blocks (like ```html or ```)
10. NEVER use backticks anywhere in your response - just return the raw HTML

**EXPECTED OUTPUT FORMAT:**
- Return complete HTML without any markdown formatting or code blocks
- The output should be valid HTML that renders properly in a browser
- Each translated text segment should appear in exactly the same HTML element it was in originally
- Tag attributes like class, id, href, src should remain unchanged
- The document structure (<html>, <head>, <body>, etc.) must remain identical

**For select/option elements:**
- Keep every <option> tag exactly as structured in the original HTML
- Translate only the visible text between <option> and </option> tags
- Don't translate the value attributes (e.g., value="00001.html")
- Example: <option value="00001.html">第1节</option> → <option value="00001.html">Section 1</option>

**For paragraph content:**
- Translate text inside <p> tags while preserving any nested tags
- Example: <p>这是<strong>重要</strong>内容</p> → <p>This is <strong>important</strong> content</p>

For translation quality:
- Render every nuance from the source into natural, fluent {target_language}
- Maintain consistent terminology throughout the document
- Preserve formatting and emphasis as indicated by HTML elements

Your task requires surgical precision: only replace the human-readable text content while leaving ALL HTML structure completely untouched. NEVER include markdown formatting or code block symbols in your response.
"""

# HTML-specific polishing prompt
HTML_POLISH_PROMPT_TEMPLATE = """
You are an expert HTML editor. Polish and improve the given **{target_language}** HTML content while perfectly preserving all HTML structure, tags, and attributes.

**CRITICAL INSTRUCTIONS:**
1. Polish ONLY the visible text content that would appear in a browser
2. DO NOT modify ANY HTML tags, attributes, or structure
3. Keep all HTML entities (like &nbsp;) unchanged
4. Preserve exact formatting, especially with select/option elements
5. Maintain the exact structure of attributes like class, id, style, etc.
6. Never add or remove HTML tags
7. Pay special attention to select/option elements - they must remain intact
8. Never modify text within script tags or HTML comments
9. DO NOT wrap your response in markdown code blocks (like ```html or ```)
10. NEVER use backticks anywhere in your response - return only raw HTML

**EXPECTED OUTPUT FORMAT:**
- Return complete HTML directly, without any markdown or code formatting
- Never include any lines starting with ``` or ending with ``` in your output
- Don't use backtick characters (`) anywhere in your response

For polishing:
- Improve fluency and readability while maintaining the original meaning
- Fix grammar, spelling, and punctuation errors
- Use natural, idiomatic {target_language}
- Ensure consistent terminology and style throughout
{style_guidance}

Your task is surgical precision: only improve the human-readable text that would be visible in a browser while leaving the HTML structure completely untouched. Return ONLY raw HTML without any markdown formatting or code block markers.
"""
