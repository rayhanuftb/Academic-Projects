"""
Statistical analysis module for educational research data analysis.

Provides hypothesis testing, correlation analysis, and regression modeling.
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Any, Tuple, Optional


class StatisticalAnalysis:
    """Performs statistical tests and modeling on educational research data."""

    @staticmethod
    def correlation_matrix(
        df: pd.DataFrame, columns: list, method: str = "pearson"
    ) -> pd.DataFrame:
        """Compute correlation matrix for specified columns."""
        valid_cols = [c for c in columns if c in df.columns]
        return df[valid_cols].corr(method=method).round(3)

    @staticmethod
    def t_test_two_groups(
        df: pd.DataFrame, numeric_col: str, group_col: str, group1: str, group2: str
    ) -> Dict[str, Any]:
        """Perform independent samples t-test between two groups."""
        g1 = df.loc[df[group_col] == group1, numeric_col].dropna()
        g2 = df.loc[df[group_col] == group2, numeric_col].dropna()

        if len(g1) < 2 or len(g2) < 2:
            return {"error": "Insufficient data in groups"}

        stat, p_value = stats.ttest_ind(g1, g2)
        cohens_d = (g1.mean() - g2.mean()) / np.sqrt(
            (g1.std() ** 2 + g2.std() ** 2) / 2
        )

        return {
            "test": "Independent Samples t-test",
            "group1": group1,
            "group2": group2,
            "group1_mean": round(float(g1.mean()), 3),
            "group2_mean": round(float(g2.mean()), 3),
            "group1_n": int(len(g1)),
            "group2_n": int(len(g2)),
            "t_statistic": round(float(stat), 4),
            "p_value": round(float(p_value), 4),
            "cohens_d": round(float(cohens_d), 3),
            "significant_at_005": bool(p_value < 0.05),
        }

    @staticmethod
    def anova_one_way(
        df: pd.DataFrame, numeric_col: str, group_col: str
    ) -> Dict[str, Any]:
        """Perform one-way ANOVA across multiple groups."""
        groups = [
            group[numeric_col].dropna().values
            for _, group in df.groupby(group_col)
            if len(group[numeric_col].dropna()) >= 2
        ]

        if len(groups) < 2:
            return {"error": "Insufficient groups for ANOVA"}

        stat, p_value = stats.f_oneway(*groups)
        eta_squared = (stat * (len(groups) - 1)) / (
            stat * (len(groups) - 1) + sum(len(g) - 1 for g in groups)
        )

        return {
            "test": "One-way ANOVA",
            "f_statistic": round(float(stat), 4),
            "p_value": round(float(p_value), 4),
            "eta_squared": round(float(eta_squared), 4),
            "n_groups": len(groups),
            "significant_at_005": bool(p_value < 0.05),
        }

    @staticmethod
    def chi_square_test(
        df: pd.DataFrame, col1: str, col2: str
    ) -> Dict[str, Any]:
        """Perform chi-square test of independence."""
        contingency = pd.crosstab(df[col1], df[col2])
        chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

        n = contingency.sum().sum()
        min_dim = min(contingency.shape) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 and n > 0 else 0

        return {
            "test": "Chi-Square Test of Independence",
            "chi2_statistic": round(float(chi2), 4),
            "p_value": round(float(p_value), 4),
            "degrees_of_freedom": int(dof),
            "cramers_v": round(float(cramers_v), 4),
            "significant_at_005": bool(p_value < 0.05),
        }

    @staticmethod
    def simple_linear_regression(
        df: pd.DataFrame, x_col: str, y_col: str
    ) -> Dict[str, Any]:
        """Perform simple linear regression."""
        clean = df[[x_col, y_col]].dropna()
        x = clean[x_col].values
        y = clean[y_col].values

        if len(x) < 3:
            return {"error": "Insufficient data for regression"}

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        return {
            "model": "Simple Linear Regression",
            "dependent": y_col,
            "independent": x_col,
            "slope": round(float(slope), 4),
            "intercept": round(float(intercept), 4),
            "r_squared": round(float(r_value ** 2), 4),
            "r_value": round(float(r_value), 4),
            "p_value": round(float(p_value), 4),
            "std_error": round(float(std_err), 4),
            "n": int(len(x)),
        }

    @staticmethod
    def pearson_correlation(
        df: pd.DataFrame, col1: str, col2: str
    ) -> Dict[str, Any]:
        """Compute Pearson correlation between two numerical columns."""
        clean = df[[col1, col2]].dropna()
        if len(clean) < 3:
            return {"error": "Insufficient data"}

        r, p_value = stats.pearsonr(clean[col1], clean[col2])
        return {
            "col1": col1,
            "col2": col2,
            "pearson_r": round(float(r), 4),
            "r_squared": round(float(r ** 2), 4),
            "p_value": round(float(p_value), 6),
            "n": int(len(clean)),
            "significant_at_005": bool(p_value < 0.05),
        }
