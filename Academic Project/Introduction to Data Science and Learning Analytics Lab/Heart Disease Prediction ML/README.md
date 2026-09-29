# Future of Cardiac Care: Predicting Heart Disease with Machine Learning

> Academic Project / Practical Work

## 📚 Course Information

- **Course Title:** Introduction to Data Science and Learning Analytics Lab
- **Course Code:** ICTE 4336
- **Student:** Rayhanul Islam
- **Institution:** University of Frontier Technology, Bangladesh

---

## ⚠️ IMPORTANT DISCLAIMER

**This project is EDUCATIONAL ONLY.** All data used is SYNTHETIC and generated for academic demonstration. This project is **NOT** a medical diagnostic tool and must **NOT** be used for clinical decisions, patient diagnosis, or treatment planning. The model performance results are based on synthetic data and do NOT reflect real-world clinical accuracy.

---

## 📌 Overview

An educational machine learning project demonstrating the complete ML pipeline for predicting heart disease risk using structured health data. The project covers data preprocessing, exploratory data analysis, model training, evaluation, and comparison.

---

## 🎯 Learning Objectives

1. Understand the complete ML pipeline from data to deployment
2. Practice data preprocessing and feature engineering
3. Train and compare multiple classification algorithms
4. Evaluate models using appropriate metrics (accuracy, precision, recall, F1, AUC-ROC)
5. Prevent data leakage through proper train/test splitting
6. Visualize data patterns and model performance

---

## 🛠️ Technologies Used

- **Language:** Python 3.10+
- **ML Libraries:** scikit-learn, XGBoost
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Testing:** pytest

---

## 📊 Models Compared

| Model | Type |
|---|---|
| Logistic Regression | Linear classifier |
| Decision Tree | Tree-based classifier |
| Random Forest | Ensemble (bagging) |
| XGBoost | Ensemble (boosting) |

---

## 📁 Project Structure

```
Heart Disease Prediction ML/
├── README.md
├── requirements.txt
├── data/
│   └── heart_disease_data.csv     (generated)
├── src/
│   ├── generate_data.py           Synthetic dataset generation
│   ├── preprocessing.py           Data cleaning & feature engineering
│   ├── models.py                  Model training & evaluation
│   ├── visualizations.py          Plot generation
│   └── main.py                    Full ML pipeline
├── tests/
│   ├── test_data.py
│   └── test_models.py
└── outputs/
    └── figures/                   Generated visualizations
```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Full Pipeline

```bash
python src/main.py
```

### 3. Run Tests

```bash
pytest tests/ -v
```

---

## 📊 Evaluation Metrics

- **Accuracy:** Overall correctness of predictions
- **Precision:** Proportion of positive predictions that are correct
- **Recall:** Proportion of actual positives correctly identified
- **F1 Score:** Harmonic mean of precision and recall
- **ROC AUC:** Area under the receiver operating characteristic curve
- **Cross-Validation:** 5-fold CV for robust performance estimation

---

## 🔒 Data Leakage Prevention

- Proper train/test split (80/20) with stratification
- Scaling fitted on training data only
- Cross-validation on training data only
- No feature engineering using test set information

---

## 🎓 Academic Note

This work was completed as part of the Introduction to Data Science and Learning Analytics Lab coursework. It demonstrates practical skills in machine learning, data preprocessing, model evaluation, and data visualization.

---

## 👤 Author

**Rayhanul Islam**  
Educational Technology and Engineering  
University of Frontier Technology, Bangladesh
