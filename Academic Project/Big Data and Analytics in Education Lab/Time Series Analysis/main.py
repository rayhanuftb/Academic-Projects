#!/usr/bin/env python3
"""
CLI Execution Script for Time Series Analysis & Forecasting.
Course: Big Data and Analytics in Education Lab (ICTE 4434)
"""

import os
import sys
import argparse
from src.pipeline import TimeSeriesPipeline


def main():
    parser = argparse.ArgumentParser(description="Educational Time Series Analysis and Forecasting Pipeline")
    parser.add_argument("--file", type=str, default=None, help="Path to input CSV dataset")
    parser.add_argument("--date-col", type=str, default="date", help="Column name containing timestamps/dates (default: 'date')")
    parser.add_argument("--target-col", type=str, default="active_users", help="Column name of the target metric (default: 'active_users')")
    parser.add_argument("--split-ratio", type=float, default=0.8, help="Train-test chronological split ratio (default: 0.8)")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Directory where forecast charts and reports are exported")

    args = parser.parse_args()

    default_dataset = os.path.join(os.path.dirname(__file__), "data", "lms_daily_student_engagement.csv")
    dataset_path = args.file if args.file else default_dataset

    print("\n==========================================================")
    print("  Time Series Analysis & Forecasting - Educational Analytics ")
    print("==========================================================")
    print(f"Dataset: {dataset_path}")
    print(f"Target Metric: {args.target_col} | Date Column: {args.date_col}")

    pipeline = TimeSeriesPipeline(output_dir=args.output_dir)

    try:
        results = pipeline.run_pipeline(
            file_path=dataset_path,
            date_column=args.date_col,
            target_column=args.target_col,
            split_ratio=args.split_ratio
        )
    except Exception as e:
        print(f"\n[!] Execution Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\n[+] Total Time Observations: {results['total_observations']} days ({results['start_date']} to {results['end_date']})")
    print(f"[+] Chronological Train Set: {results['train_size']} observations")
    print(f"[+] Chronological Test Set : {results['test_size']} observations")

    print("\n---------------- Model Forecast Evaluation ----------------")
    print(f"{'Model Name':<32} | {'MAE':<8} | {'RMSE':<8} | {'MAPE (%)':<10} | {'R^2 Score':<8}")
    print("-" * 75)
    for model_name, metrics in results['evaluations'].items():
        print(f"{model_name:<32} | {metrics['MAE']:<8.2f} | {metrics['RMSE']:<8.2f} | {metrics['MAPE_percent']:<10.2f} | {metrics['R2_Score']:<8.4f}")

    print("\n---------------- Generated Visualizations ----------------")
    for chart_label, path in results['visualizations'].items():
        print(f"  * {chart_label}: {path}")

    print(f"\n[+] Model evaluation metrics exported to: {results['metrics_csv']}")
    print(f"[+] Detailed forecast comparison exported to: {results['forecast_csv']}")
    print("Time Series analysis & forecasting completed successfully.\n")


if __name__ == "__main__":
    main()
