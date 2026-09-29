"""Tests for descriptive statistics module."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import numpy as np
import pandas as pd
import pytest
from descriptive_stats import DescriptiveStatistics


@pytest.fixture
def sample_series():
    return pd.Series([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "score": [85, 90, 78, 92, 88, 76, 95, 89, 84, 91],
        "grade": ["A", "A", "B", "A", "A", "B", "A", "A", "B", "A"],
        "group": ["X", "Y", "X", "Y", "X", "Y", "X", "Y", "X", "Y"],
    })


class TestDescriptiveStatistics:
    def setup_method(self):
        self.ds = DescriptiveStatistics()

    def test_calculate_summary_returns_dict(self, sample_series):
        result = self.ds.calculate_summary(sample_series)
        assert isinstance(result, dict)
        assert result["n"] == 10

    def test_calculate_summary_mean(self, sample_series):
        result = self.ds.calculate_summary(sample_series)
        assert result["mean"] == 55.0

    def test_calculate_summary_empty_series(self):
        result = self.ds.calculate_summary(pd.Series([], dtype=float))
        assert result == {}

    def test_calculate_summary_with_nan(self):
        s = pd.Series([1, 2, np.nan, 4, 5])
        result = self.ds.calculate_summary(s)
        assert result["n"] == 4

    def test_frequency_distribution(self, sample_df):
        result = self.ds.frequency_distribution(sample_df["grade"])
        assert result["A"] == 7
        assert result["B"] == 3

    def test_cross_tabulation(self, sample_df):
        ct = self.ds.cross_tabulation(sample_df, "grade", "group")
        assert isinstance(ct, pd.DataFrame)

    def test_full_report(self, sample_df):
        report = self.ds.full_report(
            sample_df, numerical_cols=["score"], categorical_cols=["grade"]
        )
        assert "score" in report["numerical"]
        assert "grade" in report["categorical"]
