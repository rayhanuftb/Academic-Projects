"""
Visualization module for educational research data analysis.

Generates plots and charts for data exploration and reporting.
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Optional


class ResearchVisualizer:
    """Creates visualizations for educational research data."""

    def __init__(self, output_dir: str = "outputs/figures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_theme(style="whitegrid", palette="muted")

    def _save(self, fig: plt.Figure, name: str) -> str:
        filepath = self.output_dir / f"{name}.png"
        fig.savefig(filepath, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return str(filepath)

    def plot_distribution(
        self, df: pd.DataFrame, column: str, title: Optional[str] = None
    ) -> str:
        """Plot histogram with KDE for a numerical column."""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        sns.histplot(df[column].dropna(), kde=True, ax=axes[0], color="steelblue")
        axes[0].set_title(f"Distribution of {column}")
        axes[0].set_xlabel(column)

        sns.boxplot(y=df[column].dropna(), ax=axes[1], color="steelblue")
        axes[1].set_title(f"Box Plot of {column}")

        if title:
            fig.suptitle(title, fontsize=14, fontweight="bold")
        fig.tight_layout()
        return self._save(fig, f"dist_{column}")

    def plot_categorical_counts(
        self, df: pd.DataFrame, column: str, title: Optional[str] = None
    ) -> str:
        """Plot count chart for a categorical column."""
        fig, ax = plt.subplots(figsize=(10, 5))
        order = df[column].value_counts().index
        sns.countplot(data=df, x=column, order=order, ax=ax, palette="viridis")
        ax.set_title(title or f"Frequency of {column}")
        ax.set_xlabel(column)
        ax.set_ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        fig.tight_layout()
        return self._save(fig, f"count_{column}")

    def plot_correlation_heatmap(
        self, df: pd.DataFrame, columns: List[str], title: Optional[str] = None
    ) -> str:
        """Plot correlation heatmap for numerical columns."""
        valid = [c for c in columns if c in df.columns]
        corr = df[valid].corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
        sns.heatmap(
            corr,
            mask=mask,
            annot=True,
            fmt=".2f",
            cmap="RdBu_r",
            center=0,
            ax=ax,
            square=True,
            linewidths=0.5,
        )
        ax.set_title(title or "Correlation Heatmap")
        fig.tight_layout()
        return self._save(fig, "correlation_heatmap")

    def plot_scatter(
        self,
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        hue: Optional[str] = None,
        title: Optional[str] = None,
    ) -> str:
        """Plot scatter with optional grouping."""
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue, ax=ax, alpha=0.7)
        ax.set_title(title or f"{y_col} vs {x_col}")
        fig.tight_layout()
        suffix = f"_by_{hue}" if hue else ""
        return self._save(fig, f"scatter_{x_col}_{y_col}{suffix}")

    def plot_group_comparison(
        self,
        df: pd.DataFrame,
        numeric_col: str,
        group_col: str,
        title: Optional[str] = None,
    ) -> str:
        """Plot grouped box plot for comparison."""
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df, x=group_col, y=numeric_col, ax=ax, palette="Set2")
        sns.stripplot(
            data=df, x=group_col, y=numeric_col, ax=ax,
            color="black", alpha=0.3, size=3,
        )
        ax.set_title(title or f"{numeric_col} by {group_col}")
        plt.xticks(rotation=45, ha="right")
        fig.tight_layout()
        return self._save(fig, f"group_{numeric_col}_by_{group_col}")

    def plot_missing_values(self, df: pd.DataFrame, title: Optional[str] = None) -> str:
        """Plot missing values heatmap."""
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap="YlOrRd", ax=ax)
        ax.set_title(title or "Missing Values Pattern")
        fig.tight_layout()
        return self._save(fig, "missing_values")

    def plot_bar_comparison(
        self,
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: Optional[str] = None,
    ) -> str:
        """Plot grouped bar chart."""
        fig, ax = plt.subplots(figsize=(10, 6))
        summary = df.groupby(x_col)[y_col].mean().sort_values(ascending=False)
        summary.plot(kind="bar", ax=ax, color="steelblue", edgecolor="black")
        ax.set_title(title or f"Mean {y_col} by {x_col}")
        ax.set_ylabel(f"Mean {y_col}")
        plt.xticks(rotation=45, ha="right")
        fig.tight_layout()
        return self._save(fig, f"bar_{x_col}_{y_col}")
