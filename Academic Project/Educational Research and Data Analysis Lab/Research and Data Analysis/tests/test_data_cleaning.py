"""Tests for data cleaning module."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import numpy as np
import pandas as pd
import pytest
from data_cleaning import DataCleaner


@pytest.fixture
def df_with_missing():
    return pd.DataFrame({
        "age": [20, 21, np.nan, 23, 24],
        "score": [85.0, np.nan, 78.0, 92.0, np.nan],
        "grade": ["A", "B", None, "A", "B"],
        "dept": ["CS", "Edu", "CS", None, "Edu"],
    })


@pytest.fixture
def df_with_outliers():
    return pd.DataFrame({
        "value": [10, 12, 11, 13, 100, 12, 11, 10, 200, 13]
    })


class TestDataCleaner:
    def setup_method(self):
        self.cleaner = DataCleaner()

    def test_info(self, df_with_missing):
        info = self.cleaner.info(df_with_missing)
        assert info["shape"] == (5, 4)
        assert info["missing_values"]["age"] == 1
        assert info["missing_values"]["score"] == 2

    def test_handle_missing_median(self, df_with_missing):
        result = self.cleaner.handle_missing_values(
            df_with_missing, numerical_strategy="median"
        )
        assert result.isnull().sum().sum() == 0

    def test_handle_missing_mean(self, df_with_missing):
        result = self.cleaner.handle_missing_values(
            df_with_missing, numerical_strategy="mean"
        )
        assert result.isnull().sum().sum() == 0

    def test_handle_missing_drop(self, df_with_missing):
        result = self.cleaner.handle_missing_values(
            df_with_missing, numerical_strategy="drop", categorical_strategy="drop"
        )
        assert len(result) < len(df_with_missing)

    def test_categorical_unknown(self, df_with_missing):
        result = self.cleaner.handle_missing_values(
            df_with_missing, categorical_strategy="unknown"
        )
        assert result.isnull().sum().sum() == 0

    def test_remove_outliers_iqr(self, df_with_outliers):
        result = self.cleaner.remove_outliers_iqr(df_with_outliers, ["value"])
        assert len(result) < len(df_with_outliers)
        assert result["value"].max() < 150

    def test_encode_categorical(self):
        df = pd.DataFrame({"color": ["red", "blue", "green", "red"]})
        result = self.cleaner.encode_categorical(df, ["color"])
        assert result["color"].dtype == np.int8 or result["color"].dtype.name == "int8"
