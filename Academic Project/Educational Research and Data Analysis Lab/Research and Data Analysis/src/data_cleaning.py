"""
Data cleaning module for educational research data analysis.

Provides functions to handle missing values, outliers, and data type conversions.
"""

import numpy as np
import pandas as pd
from typing import List, Optional


class DataCleaner:
    """Handles data cleaning operations for research datasets."""

    @staticmethod
    def info(df: pd.DataFrame) -> dict:
        """Return basic dataset information."""
        return {
            "shape": df.shape,
            "columns": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percent": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
        }

    @staticmethod
    def handle_missing_values(
        df: pd.DataFrame,
        numerical_strategy: str = "median",
        categorical_strategy: str = "mode",
        numerical_cols: Optional[List[str]] = None,
        categorical_cols: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Handle missing values in the dataset.

        Parameters
        ----------
        df : pd.DataFrame
            Input dataframe.
        numerical_strategy : str
            Strategy for numerical columns: 'mean', 'median', 'mode', 'drop'.
        categorical_strategy : str
            Strategy for categorical columns: 'mode', 'drop', 'unknown'.
        numerical_cols : list, optional
            List of numerical column names. If None, auto-detect.
        categorical_cols : list, optional
            List of categorical column names. If None, auto-detect.

        Returns
        -------
        pd.DataFrame
            Cleaned dataframe.
        """
        df_clean = df.copy()

        if numerical_cols is None:
            numerical_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        if categorical_cols is None:
            categorical_cols = df_clean.select_dtypes(include=["object", "category"]).columns.tolist()

        for col in numerical_cols:
            if col in df_clean.columns and df_clean[col].isnull().sum() > 0:
                if numerical_strategy == "mean":
                    df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                elif numerical_strategy == "median":
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                elif numerical_strategy == "mode":
                    mode_val = df_clean[col].mode()
                    if not mode_val.empty:
                        df_clean[col].fillna(mode_val.iloc[0], inplace=True)
                elif numerical_strategy == "drop":
                    df_clean.dropna(subset=[col], inplace=True)

        for col in categorical_cols:
            if col in df_clean.columns and df_clean[col].isnull().sum() > 0:
                if categorical_strategy == "mode":
                    mode_val = df_clean[col].mode()
                    if not mode_val.empty:
                        df_clean[col].fillna(mode_val.iloc[0], inplace=True)
                elif categorical_strategy == "unknown":
                    df_clean[col].fillna("Unknown", inplace=True)
                elif categorical_strategy == "drop":
                    df_clean.dropna(subset=[col], inplace=True)

        return df_clean

    @staticmethod
    def remove_outliers_iqr(
        df: pd.DataFrame, columns: List[str], multiplier: float = 1.5
    ) -> pd.DataFrame:
        """Remove outliers using the IQR method."""
        df_clean = df.copy()
        for col in columns:
            if col in df_clean.columns:
                q1 = df_clean[col].quantile(0.25)
                q3 = df_clean[col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - multiplier * iqr
                upper_bound = q3 + multiplier * iqr
                df_clean = df_clean[
                    (df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)
                ]
        return df_clean

    @staticmethod
    def encode_categorical(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Apply label encoding to categorical columns."""
        df_encoded = df.copy()
        for col in columns:
            if col in df_encoded.columns:
                df_encoded[col] = df_encoded[col].astype("category").cat.codes
        return df_encoded
