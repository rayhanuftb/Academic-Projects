import numpy as np
from typing import Dict, Any


class ForecastEvaluator:
    """Computes standard academic and industry forecasting evaluation metrics."""

    @staticmethod
    def calculate_mae(actual: np.ndarray, predicted: np.ndarray) -> float:
        """Mean Absolute Error (MAE)."""
        actual, predicted = np.array(actual), np.array(predicted)
        return float(np.mean(np.abs(actual - predicted)))

    @staticmethod
    def calculate_rmse(actual: np.ndarray, predicted: np.ndarray) -> float:
        """Root Mean Squared Error (RMSE)."""
        actual, predicted = np.array(actual), np.array(predicted)
        return float(np.sqrt(np.mean((actual - predicted) ** 2)))

    @staticmethod
    def calculate_mape(actual: np.ndarray, predicted: np.ndarray, epsilon: float = 1e-6) -> float:
        """
        Mean Absolute Percentage Error (MAPE) handling zero values safely using epsilon.
        Returns percentage in range [0, 100+].
        """
        actual, predicted = np.array(actual), np.array(predicted)
        denom = np.where(np.abs(actual) < epsilon, epsilon, np.abs(actual))
        mape = np.mean(np.abs((actual - predicted) / denom)) * 100.0
        return float(mape)

    @staticmethod
    def calculate_r2(actual: np.ndarray, predicted: np.ndarray) -> float:
        """Coefficient of Determination (R^2)."""
        actual, predicted = np.array(actual), np.array(predicted)
        ss_res = np.sum((actual - predicted) ** 2)
        ss_tot = np.sum((actual - np.mean(actual)) ** 2)
        if ss_tot == 0:
            return 1.0 if ss_res == 0 else 0.0
        return float(1.0 - (ss_res / ss_tot))

    @staticmethod
    def evaluate_all(actual: np.ndarray, predicted: np.ndarray) -> Dict[str, float]:
        """Calculates a comprehensive dictionary of all evaluation metrics."""
        return {
            "MAE": round(ForecastEvaluator.calculate_mae(actual, predicted), 4),
            "RMSE": round(ForecastEvaluator.calculate_rmse(actual, predicted), 4),
            "MAPE_percent": round(ForecastEvaluator.calculate_mape(actual, predicted), 2),
            "R2_Score": round(ForecastEvaluator.calculate_r2(actual, predicted), 4)
        }
