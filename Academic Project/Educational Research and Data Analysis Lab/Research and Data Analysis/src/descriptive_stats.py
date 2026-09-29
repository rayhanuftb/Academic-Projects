"""
Descriptive statistics module for educational research data analysis.

Provides comprehensive summary statistics for numerical and categorical variables.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List


class DescriptiveStatistics:
    """Computes comprehensive descriptive metrics for educational research data."""

    @staticmethod
    def calculate_summary(series: pd.Series) -> Dict[str, Any]:
        """Calculate summary statistics for a numerical series."""
        clean_series = series.dropna().astype(float)
        if clean_series.empty:
            return {}

        return {
            "n": int(len(clean_series)),
            "mean": round(float(clean_series.mean()), 3),
            "median": round(float(clean_series.median()), 3),
            "std_dev": round(float(clean_series.std()), 3),
            "variance": round(float(clean_series.var()), 3),
            "min": round(float(clean_series.min()), 3),
            "max": round(float(clean_series.max()), 3),
            "skewness": round(float(clean_series.skew()), 3),
            "kurtosis": round(float(clean_series.kurtosis()), 3),
            "q1": round(float(clean_series.quantile(0.25)), 3),
            "q3": round(float(clean_series.quantile(0.75)), 3),
            "iqr": round(float(clean_series.quantile(0.75) - clean_series.quantile(0.25)), 3),
            "range": round(float(clean_series.max() - clean_series.min()), 3),
            "cv_percent": round(float((clean_series.std() / clean_series.mean()) * 100), 3)
            if clean_series.mean() != 0
            else 0,
        }

    @staticmethod
    def frequency_distribution(series: pd.Series) -> Dict[str, int]:
        """Calculate frequency distribution for a categorical series."""
        return series.value_counts().to_dict()

    @staticmethod
    def cross_tabulation(
        df: pd.DataFrame, col1: str, col2: str
    ) -> pd.DataFrame:
        """Create a cross-tabulation between two categorical columns."""
        return pd.crosstab(df[col1], df[col2])

    def full_report(self, df: pd.DataFrame, numerical_cols: List[str], categorical_cols: List[str]) -> Dict[str, Any]:
        """Generate a full descriptive statistics report."""
        report: Dict[str, Any] = {"numerical": {}, "categorical": {}}

        for col in numerical_cols:
            if col in df.columns:
                report["numerical"][col] = self.calculate_summary(df[col])

        for col in categorical_cols:
            if col in df.columns:
                report["categorical"][col] = {
                    "frequency": self.frequency_distribution(df[col]),
                    "unique_count": int(df[col].nunique()),
                    "mode": str(df[col].mode().iloc[0]) if not df[col].mode().empty else None,
                }

        return report
