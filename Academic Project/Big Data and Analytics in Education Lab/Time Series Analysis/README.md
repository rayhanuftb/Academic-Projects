# Time Series Analysis & Forecasting

**Course:** Big Data and Analytics in Education Lab (ICTE 4434)  
**Academic Program:** B.Sc. in Educational Technology and Engineering  
**Institution:** University of Frontier Technology, Bangladesh  
**Author:** Rayhanul Islam

---

## 📌 Project Overview

This project provides a robust time series analytics and forecasting framework designed to model and predict longitudinal educational metrics (such as daily active LMS users, learning platform traffic, and student assignment submission cycles).

---

## 🎯 Key Objectives

1. **Dataset Ingestion & Validation**: Load, parse, sanitize, and chronologically sort time series data with automatic handling of missing values via linear interpolation.
2. **Rolling Statistics & Trend Analysis**: Compute moving averages (e.g., 7-day rolling window) and rolling standard deviation to establish statistical process control bands.
3. **Decomposition**: Decompose longitudinal engagement series into additive **Trend**, **Weekly Seasonality**, and **Residual Noise** components.
4. **Chronological Splitting**: Split data chronologically (80% train / 20% test) to prevent future data leakage during model training and evaluation.
5. **Multi-Model Forecasting**:
   - **Simple Moving Average (SMA)**
   - **Simple Exponential Smoothing (EMA)**
   - **Autoregressive Lag Model (AR-p)** using Ordinary Least Squares
6. **Rigorous Metric Evaluation**: Benchmark models using **MAE**, **RMSE**, **MAPE** (with zero-division protection via epsilon), and **R² Score**.
7. **Visualization & Report Generation**: Export publication-quality charts for trend analysis, component decomposition, and actual vs. predicted curves.

---

## 🏗️ Architecture & Directory Structure

```
Time Series Analysis/
├── data/
│   └── lms_daily_student_engagement.csv   # Longitudinal LMS daily engagement dataset
├── outputs/                               # Generated plots and evaluation tables
│   ├── time_series_trend.png
│   ├── trend_seasonality_decomposition.png
│   ├── actual_vs_predicted_forecast.png
│   ├── model_forecast_evaluation.csv
│   └── test_predictions_vs_actual.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py                    # CSV parsing, date indexing, interpolation
│   ├── time_series_preprocessor.py       # Rolling stats, splits, decomposition
│   ├── models.py                         # SMA, EMA, and AR forecasting models
│   ├── metrics.py                        # MAE, RMSE, MAPE, and R2 calculation
│   ├── visualizer.py                     # Matplotlib time series plotting engine
│   └── pipeline.py                       # Pipeline runner and orchestrator
├── tests/
│   └── test_time_series.py               # Automated unit & integration tests
├── main.py                               # CLI entrypoint
├── requirements.txt
└── README.md
```

---

## 📊 Sample Dataset Description

The bundled dataset [`data/lms_daily_student_engagement.csv`](./data/lms_daily_student_engagement.csv) contains 180 consecutive days of synthetic university learning management system logs.

| Column | Type | Description |
|---|---|---|
| `date` | Date (`YYYY-MM-DD`) | Daily observation timestamp |
| `active_users` | Integer | Daily count of unique authenticated student users |
| `video_hours_watched` | Integer | Aggregate hours of lecture videos streamed |
| `quiz_submissions` | Integer | Total count of objective quiz submissions |

*Note: Data generated synthetically for academic laboratory research and reproducibility.*

---

## 🚀 Installation & Execution

### 1. Prerequisites
- Python 3.9+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Pipeline on Default Dataset
```bash
python main.py
```

### 4. Run Analysis on Custom Parameters
```bash
python main.py --file data/lms_daily_student_engagement.csv --target-col active_users --split-ratio 0.8 --output-dir outputs
```

---

## 🧪 Running Automated Tests

Execute the unit and integration tests:

```bash
python -m unittest discover -s tests
```
or
```bash
pytest tests/test_time_series.py -v
```

---

## 📈 Sample Outputs

- **Time Series Trend & Rolling Band:** [`outputs/time_series_trend.png`](./outputs/time_series_trend.png)
- **Trend & Seasonality Decomposition:** [`outputs/trend_seasonality_decomposition.png`](./outputs/trend_seasonality_decomposition.png)
- **Actual vs. Predicted Forecast Comparison:** [`outputs/actual_vs_predicted_forecast.png`](./outputs/actual_vs_predicted_forecast.png)
- **Model Evaluation Summary:** [`outputs/model_forecast_evaluation.csv`](./outputs/model_forecast_evaluation.csv)
- **Test Predictions Export:** [`outputs/test_predictions_vs_actual.csv`](./outputs/test_predictions_vs_actual.csv)
