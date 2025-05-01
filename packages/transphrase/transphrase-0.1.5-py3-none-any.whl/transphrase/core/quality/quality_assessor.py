"""Quality assessment operations for translation processing"""

from typing import Dict, List, Optional, Tuple


class QualityAssessor:
    """Handles quality assessment of translations"""

    # Quality score thresholds
    QUALITY_THRESHOLDS = {
        "excellent": 9.0,
        "good": 7.5,
        "acceptable": 6.0,
        "needs_review": 4.0,
    }

    def __init__(self, config=None):
        """
        Initialize the quality assessor

        Args:
            config: Translation configuration
        """
        self.config = config

    def _assess_quality(self, source_text: str, translated_text: str) -> float:
        """
        Assess the quality of a translation using various metrics.

        Args:
            source_text: Original text
            translated_text: Translated text

        Returns:
            Quality score between 0-10
        """
        # Initialize scoring components
        scores = {
            "length_ratio": 0.0,  # How reasonable is the length ratio between source and target
            "formatting": 0.0,  # Preservation of formatting elements
            "entity_preservation": 0.0,  # Preservation of named entities, numbers, etc.
            "fluency": 0.0,  # Basic fluency checks
        }

        # 1. Length ratio check (penalize translations that are too short or too long)
        source_len = len(source_text)
        target_len = len(translated_text)

        if source_len > 0 and target_len > 0:
            ratio = target_len / source_len

            # Calculate ideal ratio based on language pair with fallbacks
            source_lang = "English"
            target_lang = "English"

            # Safely access config attributes if present
            if hasattr(self, "config") and self.config is not None:
                source_lang = getattr(self.config, "source_language", source_lang)
                target_lang = getattr(self.config, "target_language", target_lang)

            ideal_ratio = self._get_ideal_length_ratio(source_lang, target_lang)

            # Score based on how close to ideal ratio
            ratio_diff = abs(ratio - ideal_ratio)
            if ratio_diff < 0.2:
                scores["length_ratio"] = 10.0  # Very close to ideal
            elif ratio_diff < 0.5:
                scores["length_ratio"] = 8.0  # Somewhat close
            elif ratio_diff < 1.0:
                scores["length_ratio"] = 6.0  # Acceptable
            else:
                scores["length_ratio"] = 3.0  # Significantly off

        # 2. Formatting preservation
        # Check for similar paragraph structure
        source_paragraphs = source_text.count("\n\n")
        target_paragraphs = translated_text.count("\n\n")

        if source_paragraphs == 0:
            # If no paragraphs, score is perfect
            scores["formatting"] = 10.0
        else:
            para_diff = abs(source_paragraphs - target_paragraphs)
            if para_diff == 0:
                scores["formatting"] = 10.0
            elif para_diff <= 2:
                scores["formatting"] = 8.0
            elif para_diff <= 5:
                scores["formatting"] = 6.0
            else:
                scores["formatting"] = 4.0

        # 3. Entity preservation (basic check for numbers)
        source_numbers = set("".join(c for c in source_text if c.isdigit()))
        target_numbers = set("".join(c for c in translated_text if c.isdigit()))

        if not source_numbers:
            # If no numbers in source, score is perfect
            scores["entity_preservation"] = 10.0
        else:
            # Score based on number preservation
            common_digits = len(source_numbers.intersection(target_numbers))
            total_digits = len(source_numbers)

            if total_digits > 0:
                scores["entity_preservation"] = (common_digits / total_digits) * 10.0
            else:
                scores["entity_preservation"] = 10.0

        # 4. Basic fluency check (no repetitions, reasonable sentence length)
        # Check for obvious repetitions
        repetition_score = 10.0
        words = translated_text.split()
        if len(words) >= 6:  # Only check substantial text
            # Look for 3-word repetitions
            for i in range(len(words) - 5):
                trigram = " ".join(words[i : i + 3])
                if trigram in " ".join(words[i + 3 : i + 6]):
                    repetition_score -= 3.0
                    break

        # Check sentence length distribution
        sentences = [
            s.strip()
            for s in translated_text.replace("!", ".").replace("?", ".").split(".")
            if s.strip()
        ]
        if sentences:
            avg_sent_len = sum(len(s) for s in sentences) / len(sentences)
            if avg_sent_len > 300:
                # Excessively long sentences are penalized
                sentence_score = 5.0
            elif avg_sent_len < 10 and len(sentences) > 3:
                # Excessively short sentences are penalized (if there are multiple)
                sentence_score = 7.0
            else:
                sentence_score = 10.0

            scores["fluency"] = (repetition_score + sentence_score) / 2
        else:
            scores["fluency"] = repetition_score

        # Calculate weighted average
        weights = {
            "length_ratio": 0.25,
            "formatting": 0.25,
            "entity_preservation": 0.25,
            "fluency": 0.25,
        }

        weighted_score = sum(scores[k] * weights[k] for k in scores)

        # Ensure score is between 0-10
        return max(0.0, min(10.0, weighted_score))

    def _get_ideal_length_ratio(self, source_lang: str, target_lang: str) -> float:
        """
        Get ideal length ratio between source and target languages.

        Args:
            source_lang: Source language
            target_lang: Target language

        Returns:
            Ideal ratio of target/source text length
        """
        # Default 1:1 ratio
        default_ratio = 1.0

        # Known ratios for common language pairs (target/source)
        ratios = {
            ("Chinese", "English"): 1.5,  # Chinese to English expands
            ("English", "Chinese"): 0.6,  # English to Chinese contracts
            ("Japanese", "English"): 1.5,  # Japanese to English expands
            ("English", "Japanese"): 0.7,  # English to Japanese contracts
            ("Korean", "English"): 1.4,  # Korean to English expands
            ("English", "Korean"): 0.7,  # English to Korean contracts
            ("Spanish", "English"): 0.9,  # Spanish to English contracts slightly
            ("English", "Spanish"): 1.1,  # English to Spanish expands slightly
            ("German", "English"): 0.9,  # German to English contracts slightly
            ("English", "German"): 1.2,  # English to German expands
        }

        return ratios.get((source_lang, target_lang), default_ratio)

    def _calculate_quality_metrics(
        self, chunk_scores: List[float], full_source: str, full_target: str
    ) -> Dict[str, float]:
        """
        Calculate overall quality metrics from chunk scores and full text.

        Args:
            chunk_scores: Quality scores for individual chunks
            full_source: Complete source text
            full_target: Complete translated text

        Returns:
            Dictionary of quality metrics
        """
        # Calculate overall score from chunk scores (weighted by chunk length)
        if chunk_scores:
            overall_score = sum(chunk_scores) / len(chunk_scores)
        else:
            overall_score = 0.0

        # Final quality assessment
        final_assessment = {
            "overall": overall_score,
            "chunk_min": min(chunk_scores) if chunk_scores else 0.0,
            "chunk_max": max(chunk_scores) if chunk_scores else 0.0,
            "chunk_avg": overall_score,
            "sentences": len([s for s in full_target.split(".") if s.strip()]),
            "length_ratio": len(full_target) / len(full_source) if len(full_source) > 0 else 0.0,
        }

        return final_assessment

    def _get_quality_label(self, score: float) -> str:
        """
        Get a human-readable label for a quality score.

        Args:
            score: Quality score (0-10)

        Returns:
            Quality label
        """
        if score >= self.QUALITY_THRESHOLDS["excellent"]:
            return "Excellent"
        elif score >= self.QUALITY_THRESHOLDS["good"]:
            return "Good"
        elif score >= self.QUALITY_THRESHOLDS["acceptable"]:
            return "Acceptable"
        elif score >= self.QUALITY_THRESHOLDS["needs_review"]:
            return "Needs Review"
        else:
            return "Poor"
