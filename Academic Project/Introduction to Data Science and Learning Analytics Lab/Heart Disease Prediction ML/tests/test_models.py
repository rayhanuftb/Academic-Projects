"""Tests for model training and evaluation."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import numpy as np
import pandas as pd
import pytest
from generate_data import generate_heart_disease_data
from preprocessing import DataPreprocessor
from models import HeartDiseaseModeler


@pytest.fixture
def processed_data():
    df = generate_heart_disease_data(n_samples=200)
    preprocessor = DataPreprocessor()
    df_clean = preprocessor.handle_missing(df)
    X, y = preprocessor.split_features_target(df_clean)
    return X, y


class TestHeartDiseaseModeler:
    def setup_method(self):
        self.modeler = HeartDiseaseModeler(random_state=42)

    def test_split_data(self, processed_data):
        X, y = processed_data
        X_train, X_test, y_train, y_test = self.modeler.split_data(X, y)
        assert len(X_train) > len(X_test)
        assert len(y_train) == len(X_train)

    def test_train_and_evaluate(self, processed_data):
        X, y = processed_data
        X_train, X_test, y_train, y_test = self.modeler.split_data(X, y)
        results = self.modeler.train_and_evaluate(X_train, X_test, y_train, y_test)

        assert len(results) >= 3
        for name, res in results.items():
            assert "accuracy" in res
            assert "precision" in res
            assert "recall" in res
            assert "f1_score" in res
            assert "roc_auc" in res
            assert 0 <= res["accuracy"] <= 1
            assert 0 <= res["roc_auc"] <= 1

    def test_comparison_table(self, processed_data):
        X, y = processed_data
        X_train, X_test, y_train, y_test = self.modeler.split_data(X, y)
        self.modeler.train_and_evaluate(X_train, X_test, y_train, y_test)
        table = self.modeler.get_comparison_table()
        assert isinstance(table, pd.DataFrame)
        assert len(table) >= 3

    def test_best_model_selected(self, processed_data):
        X, y = processed_data
        X_train, X_test, y_train, y_test = self.modeler.split_data(X, y)
        self.modeler.train_and_evaluate(X_train, X_test, y_train, y_test)
        assert self.modeler.best_model_name != ""
        assert self.modeler.best_model is not None
