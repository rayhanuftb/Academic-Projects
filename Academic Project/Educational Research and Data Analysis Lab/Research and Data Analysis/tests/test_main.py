"""Tests for the main analysis pipeline and data generation."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import numpy as np
import pandas as pd
import pytest
from generate_dataset import generate_student_survey_data, save_dataset
from data_cleaning import DataCleaner


class TestDatasetGeneration:
    def test_generate_default(self):
        df = generate_student_survey_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 200

    def test_generate_custom_size(self):
        df = generate_student_survey_data(n_students=50)
        assert len(df) == 50

    def test_columns_present(self):
        df = generate_student_survey_data()
        expected = [
            "student_id", "age", "gender", "department",
            "year_of_study", "internet_access", "digital_literacy_score",
            "engagement_score", "study_hours_weekly", "gpa",
            "satisfaction_score", "has_laptop", "hours_on_platform_daily",
            "quiz_completion_rate",
        ]
        for col in expected:
            assert col in df.columns

    def test_has_missing_values(self):
        df = generate_student_survey_data()
        assert df.isnull().sum().sum() > 0

    def test_save_dataset(self, tmp_path):
        df = generate_student_survey_data(n_students=10)
        path = save_dataset(df, output_dir=str(tmp_path / "data"))
        assert Path(path).exists()


class TestEndToEnd:
    def test_clean_pipeline(self):
        df = generate_student_survey_data(n_students=50)
        cleaner = DataCleaner()
        df_clean = cleaner.handle_missing_values(df)
        assert df_clean.isnull().sum().sum() == 0
