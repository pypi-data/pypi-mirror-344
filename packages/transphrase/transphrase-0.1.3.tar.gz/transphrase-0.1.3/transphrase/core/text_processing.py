"""Text processing utilities for translation."""

import re
from typing import List


def split_text_semantic(text: str, max_chunk_size: int = 5000) -> List[str]:
    """
    Split text into semantic chunks respecting sentence boundaries.

    Args:
        text: The text to split
        max_chunk_size: Maximum size of each chunk

    Returns:
        List of text chunks
    """
    # If text is already small enough, return as is
    if len(text) <= max_chunk_size:
        return [text]

    # Define sentence boundaries (more comprehensive than simple splitting)
    sentence_endings = r"(?<=[.!?])\s+"
    sentences = re.split(sentence_endings, text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If a single sentence is too long, split it by comma or semicolon
        if len(sentence) > max_chunk_size:
            phrase_endings = r"(?<=[,;])\s+"
            phrases = re.split(phrase_endings, sentence)

            for phrase in phrases:
                if len(current_chunk) + len(phrase) + 2 <= max_chunk_size:
                    current_chunk += phrase + " "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())

                    # If a single phrase is still too long, force split
                    if len(phrase) > max_chunk_size:
                        # Split into fixed-size chunks, preserving words
                        words = phrase.split()
                        phrase_chunk = ""

                        for word in words:
                            if len(phrase_chunk) + len(word) + 1 <= max_chunk_size:
                                phrase_chunk += word + " "
                            else:
                                chunks.append(phrase_chunk.strip())
                                phrase_chunk = word + " "

                        if phrase_chunk:
                            current_chunk = phrase_chunk
                    else:
                        current_chunk = phrase + " "

        # Normal case - sentence fits or can be added
        elif len(current_chunk) + len(sentence) + 2 <= max_chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
