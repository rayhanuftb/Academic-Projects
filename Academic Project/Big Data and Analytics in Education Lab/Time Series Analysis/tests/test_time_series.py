import os
import sys
import unittest
import tempfile
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import TimeSeriesDataLoader
from src.time_series_preprocessor import TimeSeriesPreprocessor
from src.models import SimpleMovingAverageModel, ExponentialSmoothingModel, AutoregressiveLinearModel
from src.metrics import ForecastEvaluator
from src.pipeline import TimeSeriesPipeline


class TestTimeSeriesComponents(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        dates = pd.date_range("2026-01-01", periods=30, freq="D")
        self.sample_df = pd.DataFrame({
            "date": dates,
            "active_users": [100 + i * 2 + (10 if i % 7 < 5 else -10) for i in range(30)]
        })
        self.sample_csv = os.path.join(self.temp_dir.name, "sample_ts.csv")
        self.sample_df.to_csv(self.sample_csv, index=False)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_data_loader_valid(self):
        loaded = TimeSeriesDataLoader.load_dataset(self.sample_csv, date_column="date", target_column="active_users")
        self.assertEqual(len(loaded), 30)
        self.assertEqual(loaded.index.name, "date")
        self.assertIn("active_users", loaded.columns)

    def test_data_loader_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            TimeSeriesDataLoader.load_dataset("non_existent_file.csv")

    def test_chronological_split_no_leakage(self):
        loaded = TimeSeriesDataLoader.load_dataset(self.sample_csv, date_column="date", target_column="active_users")
        train, test = TimeSeriesPreprocessor.chronological_train_test_split(loaded, split_ratio=0.8)
        self.assertEqual(len(train), 24)
        self.assertEqual(len(test), 6)
        self.assertTrue(train.index.max() < test.index.min())

    def test_rolling_statistics(self):
        loaded = TimeSeriesDataLoader.load_dataset(self.sample_csv, date_column="date", target_column="active_users")
        rolling_df = TimeSeriesPreprocessor.calculate_rolling_statistics(loaded, "active_users", window=7)
        self.assertIn("active_users_rolling_mean_7", rolling_df.columns)
        self.assertIn("active_users_rolling_std_7", rolling_df.columns)

    def test_models_and_forecasting(self):
        train_series = pd.Series([10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0])
        steps = 4

        # SMA
        sma = SimpleMovingAverageModel(window=3).fit(train_series)
        sma_preds = sma.predict(steps=steps)
        self.assertEqual(len(sma_preds), steps)

        # EMA
        ema = ExponentialSmoothingModel(alpha=0.3).fit(train_series)
        ema_preds = ema.predict(steps=steps)
        self.assertEqual(len(ema_preds), steps)

        # AR model
        ar = AutoregressiveLinearModel(p_lags=3).fit(train_series)
        ar_preds = ar.predict(steps=steps)
        self.assertEqual(len(ar_preds), steps)

    def test_metrics_evaluation(self):
        actual = np.array([10.0, 20.0, 30.0, 40.0])
        pred = np.array([12.0, 18.0, 33.0, 38.0])

        mae = ForecastEvaluator.calculate_mae(actual, pred)
        rmse = ForecastEvaluator.calculate_rmse(actual, pred)
        mape = ForecastEvaluator.calculate_mape(actual, pred)
        r2 = ForecastEvaluator.calculate_r2(actual, pred)

        self.assertAlmostEqual(mae, 2.25, places=2)
        self.assertGreater(rmse, 0)
        self.assertGreater(mape, 0)
        self.assertGreater(r2, 0.9)

    def test_full_time_series_pipeline(self):
        pipeline = TimeSeriesPipeline(output_dir=self.temp_dir.name)
        res = pipeline.run_pipeline(self.sample_csv, date_column="date", target_column="active_users", split_ratio=0.8)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["total_observations"], 30)
        self.assertIn("Simple Moving Average (SMA-7)", res["evaluations"])
        self.assertTrue(os.path.exists(res["metrics_csv"]))
        self.assertTrue(os.path.exists(res["forecast_csv"]))


if __name__ == "__main__":
    unittest.main()
