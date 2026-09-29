"""
Visualization module for heart disease prediction project.
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional


class HeartDiseaseVisualizer:
    """Creates visualizations for the heart disease prediction project."""

    def __init__(self, output_dir: str = "outputs/figures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_theme(style="whitegrid", palette="muted")

    def _save(self, fig: plt.Figure, name: str) -> str:
        filepath = self.output_dir / f"{name}.png"
        fig.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return str(filepath)

    def plot_target_distribution(self, df: pd.DataFrame) -> str:
        """Plot target variable distribution."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        counts = df["target"].value_counts()
        labels = ["No Disease (0)", "Disease (1)"]
        colors = ["#4caf50", "#f44336"]
        axes[0].pie(counts.values, labels=labels, autopct="%1.1f%%", colors=colors)
        axes[0].set_title("Target Distribution")

        sns.countplot(data=df, x="target", ax=axes[1], palette=colors)
        axes[1].set_title("Target Count")
        axes[1].set_xlabel("Target")
        axes[1].set_ylabel("Count")

        fig.tight_layout()
        return self._save(fig, "target_distribution")

    def plot_feature_distributions(self, df: pd.DataFrame) -> str:
        """Plot distributions of numerical features."""
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if "target" in num_cols:
            num_cols.remove("target")

        n_cols = 3
        n_rows = (len(num_cols) + n_cols - 1) // n_cols
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 4))
        axes = axes.flatten() if n_rows > 1 else [axes] if n_rows == 1 else axes

        for i, col in enumerate(num_cols):
            if i < len(axes):
                sns.histplot(data=df, x=col, hue="target", kde=True, ax=axes[i], palette=["#4caf50", "#f44336"])
                axes[i].set_title(f"{col} by Target")

        for j in range(i + 1, len(axes)):
            axes[j].set_visible(False)

        fig.tight_layout()
        return self._save(fig, "feature_distributions")

    def plot_correlation_heatmap(self, df: pd.DataFrame) -> str:
        """Plot correlation heatmap."""
        fig, ax = plt.subplots(figsize=(12, 10))
        corr = df.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
        sns.heatmap(
            corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, ax=ax, square=True, linewidths=0.5, annot_kws={"size": 8},
        )
        ax.set_title("Feature Correlation Heatmap")
        fig.tight_layout()
        return self._save(fig, "correlation_heatmap")

    def plot_model_comparison(self, comparison_df: pd.DataFrame) -> str:
        """Plot model performance comparison."""
        metrics = ["Accuracy", "Precision", "Recall", "F1 Score", "ROC AUC"]
        fig, axes = plt.subplots(1, len(metrics), figsize=(20, 5))

        for i, metric in enumerate(metrics):
            sns.barplot(data=comparison_df, x="Model", y=metric, ax=axes[i], palette="Set2")
            axes[i].set_title(metric)
            axes[i].set_ylim(0.5, 1.0)
            axes[i].tick_params(axis="x", rotation=45)

        fig.suptitle("Model Performance Comparison", fontsize=14, fontweight="bold")
        fig.tight_layout()
        return self._save(fig, "model_comparison")

    def plot_confusion_matrices(self, results: Dict[str, Dict]) -> str:
        """Plot confusion matrices for all models."""
        n_models = len(results)
        fig, axes = plt.subplots(1, n_models, figsize=(5 * n_models, 5))
        if n_models == 1:
            axes = [axes]

        for i, (name, res) in enumerate(results.items()):
            cm = np.array(res["confusion_matrix"])
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[i],
                        xticklabels=["No Disease", "Disease"],
                        yticklabels=["No Disease", "Disease"])
            axes[i].set_title(f"{name}")
            axes[i].set_ylabel("True Label")
            axes[i].set_xlabel("Predicted Label")

        fig.suptitle("Confusion Matrices", fontsize=14, fontweight="bold")
        fig.tight_layout()
        return self._save(fig, "confusion_matrices")

    def plot_feature_importance(self, importance_df: pd.DataFrame) -> str:
        """Plot feature importance."""
        fig, ax = plt.subplots(figsize=(10, 8))
        top_features = importance_df.head(15)
        top_features["mean_importance"].plot(kind="barh", ax=ax, color="steelblue", edgecolor="black")
        ax.set_title("Top 15 Feature Importances (Mean across models)")
        ax.set_xlabel("Importance")
        ax.invert_yaxis()
        fig.tight_layout()
        return self._save(fig, "feature_importance")

    def plot_cv_comparison(self, comparison_df: pd.DataFrame) -> str:
        """Plot cross-validation scores comparison."""
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=comparison_df, x="Model", y="CV Mean", ax=ax, palette="Set2")
        ax.errorbar(
            range(len(comparison_df)), comparison_df["CV Mean"],
            yerr=comparison_df["CV Std"], fmt="none", color="black", capsize=5,
        )
        ax.set_title("Cross-Validation Accuracy Comparison")
        ax.set_ylabel("CV Accuracy (mean ± std)")
        ax.set_ylim(0.5, 1.0)
        ax.tick_params(axis="x", rotation=45)
        fig.tight_layout()
        return self._save(fig, "cv_comparison")
