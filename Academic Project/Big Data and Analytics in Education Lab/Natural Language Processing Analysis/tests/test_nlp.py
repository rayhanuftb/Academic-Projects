import os
import sys
import unittest
import tempfile
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocessor import TextPreprocessor
from src.analyzer import TextAnalyzer
from src.pipeline import NLPPipeline


class TestNLPPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = TextPreprocessor()

    def test_clean_text_basic(self):
        raw = "Hello World! Visit https://example.com for <b>free</b> learning."
        cleaned = self.preprocessor.clean_text(raw)
        self.assertEqual(cleaned, "hello world visit for free learning")

    def test_clean_text_empty_and_none(self):
        self.assertEqual(self.preprocessor.clean_text(""), "")
        self.assertEqual(self.preprocessor.clean_text(None), "")
        self.assertEqual(self.preprocessor.clean_text("   "), "")

    def test_tokenization_and_stopwords(self):
        text = "The course is excellent and the instructor is very helpful"
        tokens = self.preprocessor.tokenize(text)
        self.assertIn("course", tokens)
        self.assertIn("excellent", tokens)

        filtered = self.preprocessor.remove_stopwords(tokens)
        self.assertNotIn("the", filtered)
        self.assertNotIn("is", filtered)
        self.assertIn("course", filtered)
        self.assertIn("excellent", filtered)
        self.assertIn("helpful", filtered)


class TestNLPAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TextAnalyzer()

    def test_word_frequencies(self):
        tokens = ["python", "data", "python", "machine", "learning", "python", "data"]
        freqs = self.analyzer.get_word_frequencies(tokens, top_n=2)
        self.assertEqual(freqs[0], ("python", 3))
        self.assertEqual(freqs[1], ("data", 2))

    def test_ngram_generation(self):
        tokens = ["big", "data", "analytics", "education"]
        bigrams = self.analyzer.generate_ngrams(tokens, n=2)
        self.assertEqual(bigrams, ["big data", "data analytics", "analytics education"])

        trigrams = self.analyzer.generate_ngrams(tokens, n=3)
        self.assertEqual(trigrams, ["big data analytics", "data analytics education"])

    def test_sentiment_positive_and_negative(self):
        pos_tokens = ["course", "excellent", "engaging", "helpful", "material"]
        pos_res = self.analyzer.calculate_sentiment(pos_tokens)
        self.assertEqual(pos_res["label"], "Positive")
        self.assertGreater(pos_res["score"], 0)

        neg_tokens = ["class", "difficult", "confusing", "boring", "slow"]
        neg_res = self.analyzer.calculate_sentiment(neg_tokens)
        self.assertEqual(neg_res["label"], "Negative")
        self.assertLess(neg_res["score"], 0)

        neutral_tokens = ["course", "syllabus", "monday", "textbook"]
        neut_res = self.analyzer.calculate_sentiment(neutral_tokens)
        self.assertEqual(neut_res["label"], "Neutral")

    def test_vocabulary_metrics(self):
        tokens = ["apple", "banana", "apple", "cherry"]
        metrics = self.analyzer.compute_vocabulary_metrics(tokens)
        self.assertEqual(metrics["total_tokens"], 4)
        self.assertEqual(metrics["unique_tokens"], 3)
        self.assertEqual(metrics["type_token_ratio"], 0.75)


class TestNLPPipeline(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.pipeline = NLPPipeline(output_dir=self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_process_text_string(self):
        text = "This laboratory assignment on Big Data was fantastic, clear, and well structured!"
        res = self.pipeline.process_text_string(text)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["sentiment"]["label"], "Positive")
        self.assertGreater(res["vocabulary_metrics"]["total_tokens"], 0)

    def test_process_empty_string(self):
        res = self.pipeline.process_text_string("")
        self.assertEqual(res["status"], "error")

    def test_process_csv_dataset(self):
        csv_path = os.path.join(self.temp_dir.name, "test_feedback.csv")
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "course": ["Data Lab", "Data Lab", "Data Lab"],
            "feedback": [
                "The instructor was excellent and helpful",
                "The lecture was confusing and boring",
                "The class was conducted in the morning"
            ]
        })
        df.to_csv(csv_path, index=False)

        res = self.pipeline.process_file(csv_path, text_column="feedback")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["total_documents"], 3)
        self.assertEqual(res["sentiment_summary"]["Positive"], 1)
        self.assertEqual(res["sentiment_summary"]["Negative"], 1)
        self.assertEqual(res["sentiment_summary"]["Neutral"], 1)
        self.assertTrue(os.path.exists(res["output_csv"]))


if __name__ == "__main__":
    unittest.main()
