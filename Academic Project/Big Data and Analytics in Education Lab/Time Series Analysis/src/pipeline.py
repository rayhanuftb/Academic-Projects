import os
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from .data_loader import TimeSeriesDataLoader
from .time_series_preprocessor import TimeSeriesPreprocessor
from .models import SimpleMovingAverageModel, ExponentialSmoothingModel, AutoregressiveLinearModel
from .metrics import ForecastEvaluator
from .visualizer import TimeSeriesVisualizer


class TimeSeriesPipeline:
    """End-to-end time series pipeline for educational metric forecasting."""

    def __init__(self, output_dir: str = "outputs"):
        self.loader = TimeSeriesDataLoader()
        self.preprocessor = TimeSeriesPreprocessor()
        self.visualizer = TimeSeriesVisualizer(output_dir=output_dir)
        self.evaluator = ForecastEvaluator()
        self.output_dir = output_dir

    def run_pipeline(self, file_path: str, date_column: str = "date", target_column: str = "active_users", split_ratio: float = 0.8) -> Dict[str, Any]:
        """
        Executes end-to-end time series analysis, decomposition, chronological splitting,
        model training, forecasting, metric evaluation, and visualization export.
        """
        # 1. Load and clean
        df = self.loader.load_dataset(file_path, date_column=date_column, target_column=target_column)

        # 2. Rolling statistics
        df_rolling = self.preprocessor.calculate_rolling_statistics(df, target_column, window=7)

        # 3. Decomposition
        decomp = self.preprocessor.extract_trend_and_seasonality(df, target_column, period=7)

        # 4. Chronological train-test split (avoids data leakage)
        train_df, test_df = self.preprocessor.chronological_train_test_split(df, split_ratio=split_ratio)
        test_steps = len(test_df)
        actual_test = test_df[target_column].values

        # 5. Model fitting & forecasting
        models = {
            "Simple Moving Average (SMA-7)": SimpleMovingAverageModel(window=7).fit(train_df[target_column]),
            "Exponential Smoothing (EMA)": ExponentialSmoothingModel(alpha=0.35).fit(train_df[target_column]),
            "Autoregressive Model (AR-7)": AutoregressiveLinearModel(p_lags=7).fit(train_df[target_column])
        }

        predictions: Dict[str, np.ndarray] = {}
        evaluations: Dict[str, Dict[str, float]] = {}

        for name, model in models.items():
            preds = model.predict(steps=test_steps)
            predictions[name] = preds
            evaluations[name] = self.evaluator.evaluate_all(actual_test, preds)

        # 6. Generate visual artifacts
        chart_paths = {
            "time_series_trend_plot": self.visualizer.plot_time_series_and_rolling(df_rolling, target_column, window=7),
            "decomposition_plot": self.visualizer.plot_decomposition(decomp),
            "forecast_plot": self.visualizer.plot_actual_vs_predicted(train_df, test_df, predictions, target_column)
        }

        # 7. Export summary metrics to CSV
        metrics_rows = []
        for model_name, metrics in evaluations.items():
            row = {"Model": model_name}
            row.update(metrics)
            metrics_rows.append(row)
        
        metrics_df = pd.DataFrame(metrics_rows)
        metrics_csv_path = os.path.join(self.output_dir, "model_forecast_evaluation.csv")
        metrics_df.to_csv(metrics_csv_path, index=False)

        # 8. Export predicted vs actual test CSV
        forecast_export_df = pd.DataFrame({"Actual": actual_test}, index=test_df.index)
        for model_name, preds in predictions.items():
            forecast_export_df[model_name] = preds
        
        forecast_csv_path = os.path.join(self.output_dir, "test_predictions_vs_actual.csv")
        forecast_export_df.to_csv(forecast_csv_path)

        return {
            "status": "success",
            "total_observations": len(df),
            "train_size": len(train_df),
            "test_size": len(test_df),
            "start_date": str(df.index.min().date()),
            "end_date": str(df.index.max().date()),
            "evaluations": evaluations,
            "visualizations": chart_paths,
            "metrics_csv": metrics_csv_path,
            "forecast_csv": forecast_csv_path
        }
