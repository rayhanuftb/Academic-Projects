"""
Data preprocessing module for heart disease prediction.
"""

import numpy as np
import pandas as pd
from typing import Tuple, List


class DataPreprocessor:
    """Handles data cleaning and preprocessing for ML pipeline."""

    @staticmethod
    def info(df: pd.DataFrame) -> dict:
        """Return dataset information."""
        return {
            "shape": df.shape,
            "columns": list(df.columns),
            "missing": df.isnull().sum().to_dict(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "target_distribution": df["target"].value_counts().to_dict(),
        }

    @staticmethod
    def handle_missing(df: pd.DataFrame, strategy: str = "median") -> pd.DataFrame:
        """Handle missing values."""
        df_clean = df.copy()
        for col in df_clean.columns:
            if df_clean[col].isnull().sum() > 0:
                if strategy == "median":
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                elif strategy == "mean":
                    df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                elif strategy == "drop":
                    df_clean.dropna(inplace=True)
        return df_clean

    @staticmethod
    def remove_outliers_iqr(
        df: pd.DataFrame, columns: List[str], multiplier: float = 3.0
    ) -> pd.DataFrame:
        """Remove outliers using IQR method with configurable multiplier."""
        df_clean = df.copy()
        for col in columns:
            if col in df_clean.columns:
                q1 = df_clean[col].quantile(0.25)
                q3 = df_clean[col].quantile(0.75)
                iqr = q3 - q1
                lower = q1 - multiplier * iqr
                upper = q3 + multiplier * iqr
                df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]
        return df_clean

    @staticmethod
    def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
        """Add derived features."""
        df_eng = df.copy()
        df_eng["age_group"] = pd.cut(
            df_eng["age"], bins=[0, 40, 55, 70, 100], labels=["young", "middle", "senior", "elderly"]
        )
        df_eng["bps_category"] = pd.cut(
            df_eng["trestbps"], bins=[0, 120, 140, 180, 300], labels=["normal", "elevated", "high", "crisis"]
        )
        return df_eng

    @staticmethod
    def split_features_target(
        df: pd.DataFrame, target_col: str = "target"
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """Split dataframe into features and target."""
        X = df.drop(columns=[target_col])
        y = df[target_col]
        return X, y

    @staticmethod
    def scale_features(X_train: pd.DataFrame, X_test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Apply standard scaling to numerical features."""
        from sklearn.preprocessing import StandardScaler

        scaler = StandardScaler()
        num_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()

        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()

        X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
        X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])

        return X_train_scaled, X_test_scaled
