"""
Generate synthetic heart disease dataset for educational ML demonstration.

IMPORTANT: This dataset is SYNTHETIC and generated for academic purposes only.
It does NOT represent real clinical data and must NOT be used for medical diagnosis.
"""

import numpy as np
import pandas as pd
from pathlib import Path


def generate_heart_disease_data(n_samples: int = 500, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic heart disease dataset based on common clinical features.

    Parameters
    ----------
    n_samples : int
        Number of samples to generate.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pd.DataFrame
        Synthetic heart disease dataset.
    """
    np.random.seed(seed)

    age = np.random.normal(loc=55, scale=10, size=n_samples).clip(25, 80).astype(int)

    sex = np.random.choice([0, 1], size=n_samples, p=[0.35, 0.65])

    cp = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.45, 0.25, 0.15, 0.15])

    trestbps = np.random.normal(loc=130, scale=18, size=n_samples).clip(90, 200).astype(int)

    chol = np.random.normal(loc=245, scale=50, size=n_samples).clip(120, 400).astype(int)

    fbs = np.random.choice([0, 1], size=n_samples, p=[0.85, 0.15])

    restecg = np.random.choice([0, 1, 2], size=n_samples, p=[0.50, 0.30, 0.20])

    thalach = np.random.normal(loc=150, scale=22, size=n_samples).clip(70, 210).astype(int)

    exang = np.random.choice([0, 1], size=n_samples, p=[0.65, 0.35])

    oldpeak = np.random.exponential(scale=1.0, size=n_samples).clip(0, 6.2).round(1)

    slope = np.random.choice([0, 1, 2], size=n_samples, p=[0.45, 0.35, 0.20])

    ca = np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.55, 0.25, 0.12, 0.05, 0.03])

    thal = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.05, 0.35, 0.20, 0.40])

    risk_score = (
        0.03 * (age - 30)
        + 0.8 * sex
        + 0.6 * (cp == 0).astype(int)
        + 0.005 * (trestbps - 100)
        + 0.003 * (chol - 150)
        + 0.5 * exang
        + 0.3 * oldpeak
        + 0.4 * (slope == 0).astype(int)
        + 0.3 * ca
        + 0.5 * (thal == 2).astype(int)
        - 0.01 * (thalach - 120)
        + np.random.normal(0, 2, n_samples)
    )

    target = (risk_score > np.percentile(risk_score, 55)).astype(int)

    df = pd.DataFrame(
        {
            "age": age,
            "sex": sex,
            "cp": cp,
            "trestbps": trestbps,
            "chol": chol,
            "fbs": fbs,
            "restecg": restecg,
            "thalach": thalach,
            "exang": exang,
            "oldpeak": oldpeak,
            "slope": slope,
            "ca": ca,
            "thal": thal,
            "target": target,
        }
    )

    missing_idx = np.random.choice(df.index, size=int(0.02 * len(df)), replace=False)
    df.loc[missing_idx, "chol"] = np.nan

    missing_idx2 = np.random.choice(df.index, size=int(0.015 * len(df)), replace=False)
    df.loc[missing_idx2, "thalach"] = np.nan

    return df


def save_dataset(df: pd.DataFrame, output_dir: str = "data") -> str:
    """Save dataset to CSV."""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    filepath = path / "heart_disease_data.csv"
    df.to_csv(filepath, index=False)
    return str(filepath)


if __name__ == "__main__":
    df = generate_heart_disease_data()
    filepath = save_dataset(df)
    print(f"Generated {len(df)} synthetic heart disease records.")
    print(f"Dataset saved to: {filepath}")
    print(f"Target distribution:\n{df['target'].value_counts()}")
