"""
Generate synthetic dataset for educational research analysis.

IMPORTANT: This dataset is SYNTHETIC and generated for academic demonstration purposes only.
It does not represent real student data or actual research findings.
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_student_survey_data(n_students: int = 200, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic student survey data for educational research.

    The dataset simulates a survey measuring:
    - Student engagement with online learning platforms
    - Academic performance metrics
    - Demographic information
    - Technology access and digital literacy

    Parameters
    ----------
    n_students : int
        Number of synthetic student records to generate.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        DataFrame containing synthetic survey responses.
    """
    np.random.seed(seed)

    student_id = [f"STU{str(i).zfill(4)}" for i in range(1, n_students + 1)]

    age = np.random.normal(loc=20, scale=2, size=n_students).clip(17, 28).astype(int)

    gender = np.random.choice(
        ["Male", "Female", "Non-binary"],
        size=n_students,
        p=[0.48, 0.48, 0.04],
    )

    department = np.random.choice(
        ["Computer Science", "Education", "Engineering", "Business", "Sciences"],
        size=n_students,
        p=[0.25, 0.20, 0.20, 0.20, 0.15],
    )

    year_of_study = np.random.choice([1, 2, 3, 4], size=n_students, p=[0.30, 0.28, 0.24, 0.18])

    internet_access = np.random.choice(
        ["High-speed", "Moderate", "Low", "None"],
        size=n_students,
        p=[0.35, 0.35, 0.20, 0.10],
    )

    digital_literacy_score = np.random.normal(loc=65, scale=15, size=n_students).clip(10, 100).round(1)

    engagement_score = np.random.normal(loc=70, scale=12, size=n_students).clip(20, 100).round(1)

    study_hours_weekly = np.random.exponential(scale=15, size=n_students).clip(1, 60).round(1)

    gpa = np.random.normal(loc=3.0, scale=0.5, size=n_students).clip(1.0, 4.0).round(2)

    satisfaction_score = np.random.normal(loc=72, scale=14, size=n_students).clip(10, 100).round(1)

    has_laptop = np.random.choice([1, 0], size=n_students, p=[0.80, 0.20])

    hours_on_platform_daily = np.random.exponential(scale=2.5, size=n_students).clip(0, 12).round(1)

    quiz_completion_rate = np.random.normal(loc=75, scale=18, size=n_students).clip(0, 100).round(1)

    df = pd.DataFrame(
        {
            "student_id": student_id,
            "age": age,
            "gender": gender,
            "department": department,
            "year_of_study": year_of_study,
            "internet_access": internet_access,
            "digital_literacy_score": digital_literacy_score,
            "engagement_score": engagement_score,
            "study_hours_weekly": study_hours_weekly,
            "gpa": gpa,
            "satisfaction_score": satisfaction_score,
            "has_laptop": has_laptop,
            "hours_on_platform_daily": hours_on_platform_daily,
            "quiz_completion_rate": quiz_completion_rate,
        }
    )

    missing_indices = np.random.choice(df.index, size=int(0.03 * len(df)), replace=False)
    df.loc[missing_indices, "satisfaction_score"] = np.nan

    missing_indices2 = np.random.choice(df.index, size=int(0.02 * len(df)), replace=False)
    df.loc[missing_indices2, "study_hours_weekly"] = np.nan

    return df


def save_dataset(df: pd.DataFrame, output_dir: str = "data") -> str:
    """Save the DataFrame to a CSV file."""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    filepath = path / "student_survey_data.csv"
    df.to_csv(filepath, index=False)
    return str(filepath)


if __name__ == "__main__":
    df = generate_student_survey_data()
    filepath = save_dataset(df)
    print(f"Generated {len(df)} synthetic student records.")
    print(f"Dataset saved to: {filepath}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nShape: {df.shape}")
    print(f"\nFirst 5 rows:\n{df.head()}")
