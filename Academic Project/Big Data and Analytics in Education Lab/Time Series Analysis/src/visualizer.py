import os
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class TimeSeriesVisualizer:
    """Generates and exports time series plots and forecast comparison charts."""

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_time_series_and_rolling(self, df_rolling: pd.DataFrame, target_col: str, window: int = 7, filename: str = "time_series_trend.png") -> str:
        """Plots time series along with rolling mean and confidence interval band."""
        plt.figure(figsize=(12, 6))
        
        plt.plot(df_rolling.index, df_rolling[target_col], label="Daily Observed Value", color="#718096", alpha=0.6, linewidth=1.2)
        mean_col = f"{target_col}_rolling_mean_{window}"
        std_col = f"{target_col}_rolling_std_{window}"
        
        if mean_col in df_rolling.columns:
            plt.plot(df_rolling.index, df_rolling[mean_col], label=f"{window}-Day Rolling Mean", color="#2b6cb0", linewidth=2.2)
            if std_col in df_rolling.columns:
                lower = df_rolling[mean_col] - (1.96 * df_rolling[std_col])
                upper = df_rolling[mean_col] + (1.96 * df_rolling[std_col])
                plt.fill_between(df_rolling.index, lower, upper, color="#2b6cb0", alpha=0.15, label="95% Rolling Confidence Band")

        plt.title("LMS Daily Student Engagement & Traffic Over Time", fontsize=14, fontweight="bold", pad=15)
        plt.xlabel("Date Timeline", fontsize=12)
        plt.ylabel("Active User Count / Engagement Metric", fontsize=12)
        plt.legend(loc="upper left")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()

        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=200)
        plt.close()
        return output_path

    def plot_decomposition(self, decomp: Dict[str, pd.Series], filename: str = "trend_seasonality_decomposition.png") -> str:
        """Generates a 4-panel decomposition chart (Observed, Trend, Seasonal, Residuals)."""
        fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
        
        axes[0].plot(decomp["original"].index, decomp["original"], color="#2d3748", linewidth=1.5)
        axes[0].set_title("Observed Time Series", fontsize=12, fontweight="bold")
        axes[0].grid(True, linestyle="--", alpha=0.5)

        axes[1].plot(decomp["trend"].index, decomp["trend"], color="#3182ce", linewidth=2.0)
        axes[1].set_title("Estimated Trend Component", fontsize=12, fontweight="bold")
        axes[1].grid(True, linestyle="--", alpha=0.5)

        axes[2].plot(decomp["seasonal"].index, decomp["seasonal"], color="#38a169", linewidth=1.5)
        axes[2].set_title("Estimated Weekly Seasonal Component", fontsize=12, fontweight="bold")
        axes[2].grid(True, linestyle="--", alpha=0.5)

        axes[3].plot(decomp["residual"].index, decomp["residual"], color="#e53e3e", linewidth=1.0)
        axes[3].axhline(0, color="gray", linestyle="--")
        axes[3].set_title("Residual Noise", fontsize=12, fontweight="bold")
        axes[3].grid(True, linestyle="--", alpha=0.5)

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=200)
        plt.close()
        return output_path

    def plot_actual_vs_predicted(self, train_df: pd.DataFrame, test_df: pd.DataFrame, predictions: Dict[str, np.ndarray], target_col: str, filename: str = "actual_vs_predicted_forecast.png") -> str:
        """Plots chronological train, actual test, and predicted curves."""
        plt.figure(figsize=(12, 6))

        plt.plot(train_df.index, train_df[target_col], label="Train History", color="#a0aec0", linewidth=1.5)
        plt.plot(test_df.index, test_df[target_col], label="Actual Test Observed", color="#1a202c", linewidth=2.2)

        colors = ["#e53e3e", "#dd6b20", "#3182ce", "#805ad5"]
        for idx, (model_name, preds) in enumerate(predictions.items()):
            color = colors[idx % len(colors)]
            plt.plot(test_df.index, preds, label=f"Forecast ({model_name})", linestyle="--", linewidth=2.0, color=color)

        plt.title("Time Series Forecasting: Actual vs. Model Predictions", fontsize=14, fontweight="bold", pad=15)
        plt.xlabel("Date Timeline", fontsize=12)
        plt.ylabel("Student Engagement Metric", fontsize=12)
        plt.legend(loc="upper left")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()

        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=200)
        plt.close()
        return output_path
