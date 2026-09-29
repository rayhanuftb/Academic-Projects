#!/usr/bin/env python3
"""
CLI Execution Script for Natural Language Processing Analysis.
Course: Big Data and Analytics in Education Lab (ICTE 4434)
"""

import os
import sys
import argparse
from src.pipeline import NLPPipeline


def main():
    parser = argparse.ArgumentParser(description="Natural Language Processing Analysis for Educational Texts")
    parser.add_argument("--file", type=str, default=None, help="Path to input CSV or TXT file")
    parser.add_argument("--text", type=str, default=None, help="Single raw text string to analyze")
    parser.add_argument("--column", type=str, default="feedback", help="Column name containing text in CSV (default: 'feedback')")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Directory where charts and outputs will be saved")
    
    args = parser.parse_args()

    # Determine default dataset path if no argument provided
    default_dataset = os.path.join(os.path.dirname(__file__), "data", "student_course_feedback.csv")
    
    pipeline = NLPPipeline(output_dir=args.output_dir)

    if args.text:
        print("\n==========================================")
        print("  NLP Analysis - Single Text String Mode  ")
        print("==========================================")
        result = pipeline.process_text_string(args.text)
        if result["status"] == "error":
            print(f"Error: {result['message']}")
            sys.exit(1)

        print(f"Cleaned Text: {result['preprocessing']['cleaned_text']}")
        print(f"Tokens ({result['preprocessing']['token_count']}): {result['preprocessing']['filtered_tokens']}")
        print(f"Sentiment: {result['sentiment']['label']} (Score: {result['sentiment']['score']})")
        print(f"Top Words: {result['word_frequencies'][:5]}")
        print(f"Top Bigrams: {result['bigrams'][:5]}")
        print(f"Lexical Diversity (TTR): {result['vocabulary_metrics']['type_token_ratio']}")

    else:
        file_path = args.file if args.file else default_dataset
        print("\n==========================================")
        print("  NLP Analysis - Dataset Processing Mode  ")
        print("==========================================")
        print(f"Processing dataset: {file_path}")
        
        try:
            results = pipeline.process_file(file_path, text_column=args.column)
        except Exception as e:
            print(f"Execution Error: {e}", file=sys.stderr)
            sys.exit(1)

        print(f"\n[+] Total Feedback Documents Analyzed: {results['total_documents']}")
        print(f"[+] Total Vocabulary Tokens: {results['total_tokens']}")
        print(f"[+] Unique Tokens: {results['vocabulary_metrics']['unique_tokens']}")
        print(f"[+] Lexical Diversity (TTR): {results['vocabulary_metrics']['type_token_ratio']}")
        
        print("\n--- Sentiment Analysis Breakdown ---")
        for label, count in results['sentiment_summary'].items():
            pct = (count / max(results['total_documents'], 1)) * 100
            print(f"  {label:<10}: {count:>3} ({pct:5.1f}%)")

        print("\n--- Top 10 Most Frequent Words ---")
        for word, count in results['top_words'][:10]:
            print(f"  - {word:<15}: {count}")

        print("\n--- Top 5 Bigrams ---")
        for bg, count in results['top_bigrams'][:5]:
            print(f"  - {bg:<25}: {count}")

        print("\n--- Generated Visualizations ---")
        for chart_name, path in results['visualizations'].items():
            print(f"  * {chart_name}: {path}")

        print(f"\n[+] Detailed CSV report saved to: {results['output_csv']}")
        print("NLP Analysis completed successfully.\n")


if __name__ == "__main__":
    main()
