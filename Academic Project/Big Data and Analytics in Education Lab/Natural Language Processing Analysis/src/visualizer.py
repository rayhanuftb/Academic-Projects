import os
from typing import List, Tuple, Dict, Any
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless environments
import matplotlib.pyplot as plt


class NLPVisualizer:
    """Generates and exports plots for NLP analytics."""

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_word_frequencies(self, freq_list: List[Tuple[str, int]], filename: str = "word_frequency.png") -> str:
        """Plots a horizontal bar chart of top word frequencies."""
        if not freq_list:
            return ""

        words, counts = zip(*reversed(freq_list[:15]))
        plt.figure(figsize=(10, 6))
        plt.barh(words, counts, color="#2b5c8f", edgecolor="#1a365d")
        plt.title("Top Word Frequencies in Educational Feedback", fontsize=14, fontweight="bold", pad=15)
        plt.xlabel("Frequency Count", fontsize=12)
        plt.ylabel("Vocabulary Tokens", fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.6)
        plt.tight_layout()

        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=200)
        plt.close()
        return output_path

    def plot_ngrams(self, ngram_list: List[Tuple[str, int]], n: int = 2, filename: str = "ngram_distribution.png") -> str:
        """Plots top n-gram frequencies."""
        if not ngram_list:
            return ""

        ngrams, counts = zip(*reversed(ngram_list[:12]))
        plt.figure(figsize=(10, 6))
        plt.barh(ngrams, counts, color="#319795", edgecolor="#234e52")
        n_label = "Bigrams (2-word)" if n == 2 else f"{n}-grams"
        plt.title(f"Top {n_label} in Student Feedback", fontsize=14, fontweight="bold", pad=15)
        plt.xlabel("Frequency Count", fontsize=12)
        plt.ylabel("N-Gram Sequences", fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.6)
        plt.tight_layout()

        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=200)
        plt.close()
        return output_path

    def plot_sentiment_distribution(self, sentiment_counts: Dict[str, int], filename: str = "sentiment_distribution.png") -> str:
        """Plots categorical distribution of sentiment labels."""
        if not sentiment_counts or sum(sentiment_counts.values()) == 0:
            return ""

        labels = list(sentiment_counts.keys())
        sizes = list(sentiment_counts.values())
        colors = ['#38a169', '#718096', '#e53e3e']

        fig, ax = plt.subplots(figsize=(8, 6))
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=colors[:len(labels)],
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        for t in texts:
            t.set_fontsize(12)
        for at in autotexts:
            at.set_fontsize(12)
            at.set_color('white')
            at.set_weight('bold')

        plt.title("Student Feedback Sentiment Breakdown", fontsize=14, fontweight="bold", pad=15)
        plt.tight_layout()

        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=200)
        plt.close()
        return output_path
