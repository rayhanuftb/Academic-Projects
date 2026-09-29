"""
Model training and evaluation module for heart disease prediction.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
)


class HeartDiseaseModeler:
    """Trains and evaluates multiple ML models for heart disease prediction."""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models = {
            "Logistic Regression": LogisticRegression(
                max_iter=1000, random_state=random_state
            ),
            "Decision Tree": DecisionTreeClassifier(
                random_state=random_state, max_depth=8
            ),
            "Random Forest": RandomForestClassifier(
                n_estimators=100, random_state=random_state, max_depth=10
            ),
        }
        try:
            from xgboost import XGBClassifier
            self.models["XGBoost"] = XGBClassifier(
                n_estimators=100, max_depth=6, learning_rate=0.1,
                random_state=random_state, use_label_encoder=False,
                eval_metric="logloss",
            )
        except ImportError:
            pass

        self.results: Dict[str, Dict[str, Any]] = {}
        self.best_model_name: str = ""
        self.best_model = None

    def split_data(
        self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2
    ) -> Tuple:
        """Split data into train/test sets."""
        return train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )

    def train_and_evaluate(
        self, X_train: pd.DataFrame, X_test: pd.DataFrame,
        y_train: pd.Series, y_test: pd.Series
    ) -> Dict[str, Dict[str, Any]]:
        """Train all models and evaluate performance."""
        best_auc = 0

        for name, model in self.models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, zero_division=0)
            recall = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            auc = roc_auc_score(y_test, y_proba)

            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")

            self.results[name] = {
                "accuracy": round(float(accuracy), 4),
                "precision": round(float(precision), 4),
                "recall": round(float(recall), 4),
                "f1_score": round(float(f1), 4),
                "roc_auc": round(float(auc), 4),
                "cv_mean": round(float(cv_scores.mean()), 4),
                "cv_std": round(float(cv_scores.std()), 4),
                "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
                "classification_report": classification_report(
                    y_test, y_pred, output_dict=True
                ),
            }

            if auc > best_auc:
                best_auc = auc
                self.best_model_name = name
                self.best_model = model

        return self.results

    def get_comparison_table(self) -> pd.DataFrame:
        """Return a comparison DataFrame of all models."""
        rows = []
        for name, res in self.results.items():
            rows.append({
                "Model": name,
                "Accuracy": res["accuracy"],
                "Precision": res["precision"],
                "Recall": res["recall"],
                "F1 Score": res["f1_score"],
                "ROC AUC": res["roc_auc"],
                "CV Mean": res["cv_mean"],
                "CV Std": res["cv_std"],
            })
        return pd.DataFrame(rows)

    def get_feature_importance(self, feature_names: list) -> pd.DataFrame:
        """Get feature importance from tree-based models."""
        importance_data = {}
        for name, model in self.models.items():
            if hasattr(model, "feature_importances_"):
                importance_data[name] = model.feature_importances_

        if not importance_data:
            return pd.DataFrame()

        df_imp = pd.DataFrame(importance_data, index=feature_names)
        df_imp["mean_importance"] = df_imp.mean(axis=1)
        return df_imp.sort_values("mean_importance", ascending=False)
