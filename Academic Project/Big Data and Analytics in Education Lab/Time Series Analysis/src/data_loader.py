import os
import pandas as pd
from typing import Optional, Tuple


class TimeSeriesDataLoader:
    """Loads, validates, and sorts time series datasets."""

    @staticmethod
    def load_dataset(file_path: str, date_column: str = "date", target_column: str = "active_users") -> pd.DataFrame:
        """
        Loads CSV dataset, parses date column, checks required columns,
        sorts chronologically, and sets DateTimeIndex.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Time series dataset not found at: {file_path}")

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Failed to read CSV dataset: {str(e)}")

        if df.empty:
            raise ValueError("Provided dataset is empty.")

        if date_column not in df.columns:
            # Attempt to find a column with 'date' or 'time' in name
            date_candidates = [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower() or 'day' in c.lower()]
            if not date_candidates:
                raise ValueError(f"Date column '{date_column}' not found in dataset columns: {list(df.columns)}")
            date_column = date_candidates[0]

        if target_column not in df.columns:
            # Fallback to the first numeric column that is not the date
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if not numeric_cols:
                raise ValueError(f"Target column '{target_column}' not found and no numeric columns available.")
            target_column = numeric_cols[0]

        # Parse date and sort
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        # Drop rows with unparseable dates
        df = df.dropna(subset=[date_column])
        if df.empty:
            raise ValueError("All date values were invalid or unparseable.")

        df = df.sort_values(by=date_column).reset_index(drop=True)
        df.set_index(date_column, inplace=True)

        # Handle missing values in target column using linear interpolation and forward fill
        if df[target_column].isna().sum() > 0:
            df[target_column] = df[target_column].interpolate(method='linear').bfill().ffill()

        return df[[target_column]]
