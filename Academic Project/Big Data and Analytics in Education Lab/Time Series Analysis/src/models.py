import numpy as np
import pandas as pd
from typing import Dict, Any, List


class SimpleMovingAverageModel:
    """Moving average forecasting model."""

    def __init__(self, window: int = 7):
        self.window = window
        self.last_values: List[float] = []

    def fit(self, train_series: pd.Series):
        self.last_values = train_series.tolist()[-self.window:]
        return self

    def predict(self, steps: int) -> np.ndarray:
        history = list(self.last_values)
        predictions = []
        for _ in range(steps):
            pred = float(np.mean(history[-self.window:]))
            predictions.append(pred)
            history.append(pred)
        return np.array(predictions)


class ExponentialSmoothingModel:
    """Simple Exponential Smoothing (SES) forecasting model."""

    def __init__(self, alpha: float = 0.3):
        self.alpha = alpha
        self.level: float = 0.0

    def fit(self, train_series: pd.Series):
        values = train_series.values
        if len(values) == 0:
            self.level = 0.0
            return self
        
        # Initialize level
        level = values[0]
        for val in values[1:]:
            level = self.alpha * val + (1 - self.alpha) * level
        self.level = float(level)
        return self

    def predict(self, steps: int) -> np.ndarray:
        return np.full(shape=(steps,), fill_value=self.level)


class AutoregressiveLinearModel:
    """Autoregressive (AR-p) forecasting model using Ordinary Least Squares."""

    def __init__(self, p_lags: int = 7):
        self.p_lags = p_lags
        self.weights: np.ndarray = np.array([])
        self.intercept: float = 0.0
        self.history: List[float] = []

    def fit(self, train_series: pd.Series):
        values = train_series.values.astype(float)
        self.history = list(values)
        
        n = len(values)
        if n <= self.p_lags:
            # Fallback if series is shorter than lags
            self.p_lags = max(1, n // 2)
        
        # Construct lag matrix X and target y
        X = []
        y = []
        for i in range(self.p_lags, n):
            X.append(values[i - self.p_lags:i][::-1])  # lag 1, lag 2, ... lag p
            y.append(values[i])
        
        X = np.array(X)
        y = np.array(y)

        # Add bias term (column of 1s)
        X_with_bias = np.hstack([np.ones((X.shape[0], 1)), X])
        
        # Solve OLS: theta = (X^T X)^-1 X^T y
        try:
            theta, residuals, rank, s = np.linalg.lstsq(X_with_bias, y, rcond=None)
            self.intercept = theta[0]
            self.weights = theta[1:]
        except Exception:
            self.intercept = float(np.mean(values))
            self.weights = np.zeros(self.p_lags)

        return self

    def predict(self, steps: int) -> np.ndarray:
        hist = list(self.history)
        preds = []
        for _ in range(steps):
            lags = np.array(hist[-self.p_lags:][::-1])
            pred = self.intercept + np.dot(self.weights, lags)
            # Bound prediction to non-negative if historical data was non-negative
            if all(v >= 0 for v in hist):
                pred = max(0.0, float(pred))
            preds.append(float(pred))
            hist.append(pred)
        return np.array(preds)
