import re
import string
from typing import List, Dict, Any, Optional

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    # Ensure stopwords are available if downloaded
    try:
        STOPWORDS_SET = set(stopwords.words('english'))
    except Exception:
        STOPWORDS_SET = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
            "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
            'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
            'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
            'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
            'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
            'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',
            'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
            'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
            'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll',
            'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',
            "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven',
            "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't",
            'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't",
            'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
        }
except ImportError:
    STOPWORDS_SET = {
        'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'she', 'it', 'they',
        'the', 'a', 'an', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
        'which', 'this', 'that', 'these', 'those', 'is', 'are', 'was', 'were',
        'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'to', 'from',
        'in', 'out', 'on', 'off', 'over', 'under', 'with', 'at', 'by', 'for'
    }


class TextPreprocessor:
    """Preprocesses raw educational and natural language texts."""

    def __init__(self, custom_stopwords: Optional[set] = None):
        self.stopwords = custom_stopwords if custom_stopwords is not None else STOPWORDS_SET
        self.stemmer = PorterStemmer() if 'PorterStemmer' in globals() else None

    def clean_text(self, text: Optional[str]) -> str:
        """Sanitizes text by removing HTML tags, URLs, numbers, and extra whitespace."""
        if not text or not isinstance(text, str):
            return ""
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        # Remove HTML tags
        text = re.sub(r'<.*?>', ' ', text)
        # Remove non-alphabetical characters except standard spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        # Normalize whitespace and lowercase
        text = re.sub(r'\s+', ' ', text).strip().lower()
        return text

    def tokenize(self, text: Optional[str]) -> List[str]:
        """Splits cleaned text into alphanumeric word tokens."""
        cleaned = self.clean_text(text)
        if not cleaned:
            return []
        return cleaned.split()

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Filters out common English stopwords from token list."""
        if not tokens:
            return []
        return [t for t in tokens if t not in self.stopwords and len(t) > 1]

    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Applies Porter Stemming to word tokens."""
        if not tokens:
            return []
        if self.stemmer:
            return [self.stemmer.stem(t) for t in tokens]
        return tokens

    def preprocess_pipeline(self, text: Optional[str], stem: bool = False) -> Dict[str, Any]:
        """Full pipeline returning cleaned text, raw tokens, and filtered tokens."""
        cleaned = self.clean_text(text)
        raw_tokens = self.tokenize(cleaned)
        filtered_tokens = self.remove_stopwords(raw_tokens)
        processed_tokens = self.stem_tokens(filtered_tokens) if stem else filtered_tokens
        
        return {
            "original_length": len(text) if isinstance(text, str) else 0,
            "cleaned_text": cleaned,
            "raw_tokens": raw_tokens,
            "filtered_tokens": filtered_tokens,
            "processed_tokens": processed_tokens,
            "token_count": len(filtered_tokens)
        }
