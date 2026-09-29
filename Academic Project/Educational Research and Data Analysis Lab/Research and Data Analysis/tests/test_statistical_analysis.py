"""Tests for statistical analysis module."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import numpy as np
import pandas as pd
import pytest
from statistical_analysis import StatisticalAnalysis


@pytest.fixture
def analysis_df():
    np.random.seed(42)
    n = 100
    return pd.DataFrame({
        "score": np.random.normal(75, 10, n),
        "hours": np.random.exponential(10, n),
        "gpa": np.random.normal(3.0, 0.5, n),
        "dept": np.random.choice(["CS", "Edu", "Eng"], n),
        "gender": np.random.choice(["M", "F"], n),
        "pass": np.random.choice(["Pass", "Fail"], n, p=[0.8, 0.2]),
    })


class TestStatisticalAnalysis:
    def setup_method(self):
        self.sa = StatisticalAnalysis()

    def test_correlation_matrix(self, analysis_df):
        result = self.sa.correlation_matrix(analysis_df, ["score", "hours", "gpa"])
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (3, 3)

    def test_t_test(self, analysis_df):
        result = self.sa.t_test_two_groups(
            analysis_df, "score", "gender", "M", "F"
        )
        assert "t_statistic" in result
        assert "p_value" in result
        assert "cohens_d" in result
        assert isinstance(result["significant_at_005"], bool)

    def test_t_test_insufficient_data(self):
        df = pd.DataFrame({"score": [1], "group": ["A"]})
        result = self.sa.t_test_two_groups(df, "score", "group", "A", "B")
        assert "error" in result

    def test_anova(self, analysis_df):
        result = self.sa.anova_one_way(analysis_df, "score", "dept")
        assert "f_statistic" in result
        assert "p_value" in result
        assert "eta_squared" in result

    def test_chi_square(self, analysis_df):
        result = self.sa.chi_square_test(analysis_df, "dept", "pass")
        assert "chi2_statistic" in result
        assert "cramers_v" in result

    def test_simple_linear_regression(self, analysis_df):
        result = self.sa.simple_linear_regression(
            analysis_df, "hours", "score"
        )
        assert "slope" in result
        assert "r_squared" in result
        assert 0 <= result["r_squared"] <= 1

    def test_pearson_correlation(self, analysis_df):
        result = self.sa.pearson_correlation(analysis_df, "hours", "gpa")
        assert "pearson_r" in result
        assert -1 <= result["pearson_r"] <= 1
