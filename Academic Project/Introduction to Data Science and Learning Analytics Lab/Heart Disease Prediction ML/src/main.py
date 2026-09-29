"""
Main analysis script for Heart Disease Prediction ML project.

This script demonstrates the complete ML pipeline:
1. Data generation (synthetic)
2. Exploratory Data Analysis
3. Data preprocessing
4. Model training and evaluation
5. Model comparison and visualization

IMPORTANT: All data is SYNTHETIC. This project is EDUCATIONAL only.
It is NOT a medical diagnostic tool and must NOT be used for clinical decisions.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate_data import generate_heart_disease_data, save_dataset
from preprocessing import DataPreprocessor
from models import HeartDiseaseModeler
from visualizations import HeartDiseaseVisualizer


def run_pipeline():
    """Execute the complete ML pipeline."""
    print("=" * 70)
    print("HEART DISEASE PREDICTION WITH MACHINE LEARNING")
    print("Educational Project - Synthetic Data Only")
    print("=" * 70)

    print("\n[1] Generating synthetic dataset...")
    df = generate_heart_disease_data(n_samples=500)
    data_path = save_dataset(df)
    print(f"    Dataset saved to: {data_path}")
    print(f"    Shape: {df.shape}")

    print("\n[2] Exploratory Data Analysis...")
    preprocessor = DataPreprocessor()
    info = preprocessor.info(df)
    print(f"    Features: {info['shape'][1] - 1}")
    print(f"    Samples: {info['shape'][0]}")
    print(f"    Missing values: {sum(info['missing'].values())}")
    print(f"    Target distribution: {info['target_distribution']}")

    viz = HeartDiseaseVisualizer(output_dir="outputs/figures")

    fig1 = viz.plot_target_distribution(df)
    print(f"    Saved: {fig1}")

    fig2 = viz.plot_feature_distributions(df)
    print(f"    Saved: {fig2}")

    fig3 = viz.plot_correlation_heatmap(df)
    print(f"    Saved: {fig3}")

    print("\n[3] Data Preprocessing...")
    df_clean = preprocessor.handle_missing(df, strategy="median")
    df_clean = preprocessor.remove_outliers_iqr(df_clean, ["trestbps", "chol", "thalach"])

    X, y = preprocessor.split_features_target(df_clean)
    print(f"    Features shape: {X.shape}")
    print(f"    Target shape: {y.shape}")

    print("\n[4] Training and Evaluating Models...")
    modeler = HeartDiseaseModeler(random_state=42)
    X_train, X_test, y_train, y_test = modeler.split_data(X, y, test_size=0.2)
    print(f"    Train size: {X_train.shape[0]}")
    print(f"    Test size: {X_test.shape[0]}")

    X_train_scaled, X_test_scaled = preprocessor.scale_features(X_train, X_test)

    results = modeler.train_and_evaluate(X_train_scaled, X_test_scaled, y_train, y_test)

    print("\n[5] Model Comparison:")
    print("    " + "-" * 90)
    comparison = modeler.get_comparison_table()
    print(comparison.to_string(index=False))
    print("    " + "-" * 90)
    print(f"\n    Best Model: {modeler.best_model_name} "
          f"(AUC = {results[modeler.best_model_name]['roc_auc']})")

    print("\n[6] Generating Visualizations...")
    fig4 = viz.plot_model_comparison(comparison)
    print(f"    Saved: {fig4}")

    fig5 = viz.plot_confusion_matrices(results)
    print(f"    Saved: {fig5}")

    fig6 = viz.plot_cv_comparison(comparison)
    print(f"    Saved: {fig6}")

    importance_df = modeler.get_feature_importance(list(X.columns))
    if not importance_df.empty:
        fig7 = viz.plot_feature_importance(importance_df)
        print(f"    Saved: {fig7}")

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)
    print("\nThis is an EDUCATIONAL project using SYNTHETIC data.")
    print("NOT for clinical use or medical diagnosis.")


if __name__ == "__main__":
    run_pipeline()
