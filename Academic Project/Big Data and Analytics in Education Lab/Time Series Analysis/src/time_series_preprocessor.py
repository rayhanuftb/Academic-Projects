import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any


class TimeSeriesPreprocessor:
    """Computes time series transformations, rolling statistics, and chronological splits."""

    @staticmethod
    def calculate_rolling_statistics(df: pd.DataFrame, target_column: str, window: int = 7) -> pd.DataFrame:
        """Computes rolling mean and rolling standard deviation."""
        res_df = df.copy()
        res_df[f'{target_column}_rolling_mean_{window}'] = res_df[target_column].rolling(window=window, min_periods=1).mean()
        res_df[f'{target_column}_rolling_std_{window}'] = res_df[target_column].rolling(window=window, min_periods=1).std().fillna(0)
        return res_df

    @staticmethod
    def chronological_train_test_split(df: pd.DataFrame, split_ratio: float = 0.8) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Splits time series chronologically without shuffling to prevent future data leakage.
        """
        if df.empty or len(df) < 5:
            raise ValueError("Dataset too small for train-test split (minimum 5 observations required).")

        split_idx = int(len(df) * split_ratio)
        if split_idx == 0 or split_idx >= len(df):
            split_idx = max(1, len(df) - 1)

        train_df = df.iloc[:split_idx].copy()
        test_df = df.iloc[split_idx:].copy()
        return train_df, test_df

    @staticmethod
    def extract_trend_and_seasonality(df: pd.DataFrame, target_column: str, period: int = 7) -> Dict[str, pd.Series]:
        """
        Decomposes series into simple additive components (Trend, Seasonality, Residuals).
        """
        series = df[target_column]
        # Trend using symmetric centered moving average
        trend = series.rolling(window=period, center=True, min_periods=1).mean()
        detrended = series - trend
        
        # Day of week or periodic seasonal factor
        seasonal_means = detrended.groupby(detrended.index.dayofweek if hasattr(detrended.index, 'dayofweek') else (np.arange(len(series)) % period)).transform('mean')
        residuals = detrended - seasonal_means

        return {
            "original": series,
            "trend": trend,
            "seasonal": seasonal_means,
            "residual": residuals
        }
