from collections import Counter
from typing import List, Dict, Tuple, Any, Optional

# Lexicon for rule-based educational sentiment scoring
POSITIVE_WORDS = {
    'excellent', 'great', 'good', 'helpful', 'engaging', 'clear', 'enjoyed',
    'loved', 'fantastic', 'informative', 'valuable', 'interesting', 'effective',
    'supportive', 'inspiring', 'well', 'structured', 'friendly', 'best',
    'organized', 'easy', 'interactive', 'positive', 'thorough', 'brilliant',
    'enriching', 'rewarding', 'practical', 'useful', 'comprehensive', 'satisfied'
}

NEGATIVE_WORDS = {
    'difficult', 'confusing', 'hard', 'poor', 'bad', 'boring', 'unclear',
    'disorganized', 'slow', 'frustrating', 'useless', 'unfair', 'delayed',
    'vague', 'stressful', 'monotonous', 'complicated', 'harsh', 'worst',
    'terrible', 'disappointed', 'ineffective', 'lacking', 'unhelpful', 'unresponsive'
}


class TextAnalyzer:
    """Performs statistical, n-gram, and sentiment analysis on processed tokens."""

    @staticmethod
    def get_word_frequencies(tokens: List[str], top_n: int = 20) -> List[Tuple[str, int]]:
        """Returns the top N most frequent words."""
        if not tokens:
            return []
        counter = Counter(tokens)
        return counter.most_common(top_n)

    @staticmethod
    def generate_ngrams(tokens: List[str], n: int = 2) -> List[str]:
        """Generates n-grams (sequences of n consecutive words) from token list."""
        if not tokens or len(tokens) < n or n < 1:
            return []
        ngrams = [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]
        return ngrams

    @staticmethod
    def get_ngram_frequencies(tokens: List[str], n: int = 2, top_n: int = 15) -> List[Tuple[str, int]]:
        """Returns the top N most frequent n-grams."""
        ngrams = TextAnalyzer.generate_ngrams(tokens, n=n)
        if not ngrams:
            return []
        return Counter(ngrams).most_common(top_n)

    @staticmethod
    def calculate_sentiment(tokens: List[str]) -> Dict[str, Any]:
        """
        Calculates sentiment polarity using domain-weighted lexicon matching.
        Returns score in range [-1.0, 1.0] and a categorical label.
        """
        if not tokens:
            return {
                "score": 0.0,
                "label": "Neutral",
                "positive_matches": [],
                "negative_matches": [],
                "positive_count": 0,
                "negative_count": 0
            }

        pos_matches = [w for w in tokens if w in POSITIVE_WORDS]
        neg_matches = [w for w in tokens if w in NEGATIVE_WORDS]

        pos_count = len(pos_matches)
        neg_count = len(neg_matches)
        total_matched = pos_count + neg_count

        if total_matched == 0:
            score = 0.0
            label = "Neutral"
        else:
            score = round((pos_count - neg_count) / max(total_matched, 1), 3)
            if score > 0.15:
                label = "Positive"
            elif score < -0.15:
                label = "Negative"
            else:
                label = "Neutral"

        return {
            "score": score,
            "label": label,
            "positive_matches": pos_matches,
            "negative_matches": neg_matches,
            "positive_count": pos_count,
            "negative_count": neg_count
        }

    @staticmethod
    def compute_vocabulary_metrics(tokens: List[str]) -> Dict[str, float]:
        """Computes lexical diversity (Type-Token Ratio) and vocabulary size."""
        if not tokens:
            return {"total_tokens": 0, "unique_tokens": 0, "type_token_ratio": 0.0}
        
        total = len(tokens)
        unique = len(set(tokens))
        ttr = round(unique / total, 4) if total > 0 else 0.0

        return {
            "total_tokens": total,
            "unique_tokens": unique,
            "type_token_ratio": ttr
        }
