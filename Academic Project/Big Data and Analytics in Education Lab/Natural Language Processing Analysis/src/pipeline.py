import os
import pandas as pd
from typing import Dict, Any, List, Optional
from .preprocessor import TextPreprocessor
from .analyzer import TextAnalyzer
from .visualizer import NLPVisualizer


class NLPPipeline:
    """End-to-end NLP analytics pipeline for educational text corpora."""

    def __init__(self, output_dir: str = "outputs"):
        self.preprocessor = TextPreprocessor()
        self.analyzer = TextAnalyzer()
        self.visualizer = NLPVisualizer(output_dir=output_dir)
        self.output_dir = output_dir

    def process_text_string(self, text: str) -> Dict[str, Any]:
        """Runs the pipeline on a single text string."""
        if not text or not text.strip():
            return {
                "status": "error",
                "message": "Input text is empty."
            }

        prep_result = self.preprocessor.preprocess_pipeline(text)
        tokens = prep_result["filtered_tokens"]
        word_freqs = self.analyzer.get_word_frequencies(tokens, top_n=15)
        bigrams = self.analyzer.get_ngram_frequencies(tokens, n=2, top_n=10)
        trigrams = self.analyzer.get_ngram_frequencies(tokens, n=3, top_n=5)
        sentiment = self.analyzer.calculate_sentiment(tokens)
        vocab_metrics = self.analyzer.compute_vocabulary_metrics(tokens)

        return {
            "status": "success",
            "preprocessing": prep_result,
            "word_frequencies": word_freqs,
            "bigrams": bigrams,
            "trigrams": trigrams,
            "sentiment": sentiment,
            "vocabulary_metrics": vocab_metrics
        }

    def process_file(self, file_path: str, text_column: str = "feedback") -> Dict[str, Any]:
        """Loads a CSV or TXT file, analyzes all entries, aggregates results, and generates visualizations."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at: {file_path}")

        all_tokens: List[str] = []
        sentiment_summary = {"Positive": 0, "Neutral": 0, "Negative": 0}
        analyzed_rows = []

        if file_path.endswith('.csv'):
            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                raise ValueError(f"Failed to read CSV file: {str(e)}")

            if text_column not in df.columns:
                # Fallback to the first string/object column
                text_cols = [c for c in df.columns if df[c].dtype == object]
                if not text_cols:
                    raise ValueError(f"No suitable text column found in CSV. Expected '{text_column}'.")
                text_column = text_cols[0]

            for idx, row in df.iterrows():
                text_val = str(row[text_column]) if pd.notna(row[text_column]) else ""
                tokens = self.preprocessor.remove_stopwords(self.preprocessor.tokenize(text_val))
                sent = self.analyzer.calculate_sentiment(tokens)
                sentiment_summary[sent["label"]] = sentiment_summary.get(sent["label"], 0) + 1
                all_tokens.extend(tokens)
                analyzed_rows.append({
                    "id": row.get("id", idx + 1),
                    "course": row.get("course", "Unknown"),
                    "text": text_val,
                    "sentiment_score": sent["score"],
                    "sentiment_label": sent["label"]
                })
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            for idx, line in enumerate(lines):
                line_clean = line.strip()
                if not line_clean:
                    continue
                tokens = self.preprocessor.remove_stopwords(self.preprocessor.tokenize(line_clean))
                sent = self.analyzer.calculate_sentiment(tokens)
                sentiment_summary[sent["label"]] = sentiment_summary.get(sent["label"], 0) + 1
                all_tokens.extend(tokens)
                analyzed_rows.append({
                    "id": idx + 1,
                    "text": line_clean,
                    "sentiment_score": sent["score"],
                    "sentiment_label": sent["label"]
                })

        # Aggregated statistics
        top_words = self.analyzer.get_word_frequencies(all_tokens, top_n=20)
        top_bigrams = self.analyzer.get_ngram_frequencies(all_tokens, n=2, top_n=15)
        top_trigrams = self.analyzer.get_ngram_frequencies(all_tokens, n=3, top_n=10)
        vocab_metrics = self.analyzer.compute_vocabulary_metrics(all_tokens)

        # Generate and save visual plots
        chart_paths = {}
        if top_words:
            chart_paths["word_freq_plot"] = self.visualizer.plot_word_frequencies(top_words)
        if top_bigrams:
            chart_paths["bigram_plot"] = self.visualizer.plot_ngrams(top_bigrams, n=2)
        if sum(sentiment_summary.values()) > 0:
            chart_paths["sentiment_plot"] = self.visualizer.plot_sentiment_distribution(sentiment_summary)

        # Export detailed analysis CSV
        output_csv = os.path.join(self.output_dir, "feedback_sentiment_analysis.csv")
        pd.DataFrame(analyzed_rows).to_csv(output_csv, index=False)

        return {
            "status": "success",
            "total_documents": len(analyzed_rows),
            "total_tokens": len(all_tokens),
            "vocabulary_metrics": vocab_metrics,
            "top_words": top_words,
            "top_bigrams": top_bigrams,
            "top_trigrams": top_trigrams,
            "sentiment_summary": sentiment_summary,
            "visualizations": chart_paths,
            "output_csv": output_csv
        }
