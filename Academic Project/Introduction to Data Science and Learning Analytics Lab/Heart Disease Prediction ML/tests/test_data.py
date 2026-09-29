"""Tests for data generation and preprocessing modules."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import numpy as np
import pandas as pd
import pytest
from generate_data import generate_heart_disease_data, save_dataset
from preprocessing import DataPreprocessor


class TestGenerateData:
    def test_default_generation(self):
        df = generate_heart_disease_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 500

    def test_custom_samples(self):
        df = generate_heart_disease_data(n_samples=100)
        assert len(df) == 100

    def test_columns_present(self):
        df = generate_heart_disease_data()
        expected_cols = [
            "age", "sex", "cp", "trestbps", "chol", "fbs",
            "restecg", "thalach", "exang", "oldpeak", "slope",
            "ca", "thal", "target",
        ]
        for col in expected_cols:
            assert col in df.columns

    def test_target_binary(self):
        df = generate_heart_disease_data()
        assert set(df["target"].unique()).issubset({0, 1})

    def test_has_missing(self):
        df = generate_heart_disease_data()
        assert df.isnull().sum().sum() > 0

    def test_save(self, tmp_path):
        df = generate_heart_disease_data(n_samples=10)
        path = save_dataset(df, output_dir=str(tmp_path / "data"))
        assert Path(path).exists()


class TestPreprocessor:
    def setup_method(self):
        self.preprocessor = DataPreprocessor()

    def test_handle_missing(self):
        df = generate_heart_disease_data()
        df_clean = self.preprocessor.handle_missing(df)
        assert df_clean.isnull().sum().sum() == 0

    def test_split_features_target(self):
        df = generate_heart_disease_data(n_samples=50)
        X, y = self.preprocessor.split_features_target(df)
        assert "target" not in X.columns
        assert len(y) == len(df)

    def test_info(self):
        df = generate_heart_disease_data(n_samples=50)
        info = self.preprocessor.info(df)
        assert info["shape"] == (50, 14)
