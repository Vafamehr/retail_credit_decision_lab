# src/response_modeling/evaluate_response_model.py

from sklearn.metrics import roc_auc_score
import numpy as np


def evaluate_response_model(y_true, y_pred_proba):
    """
    Evaluate response model performance.

    Inputs:
        y_true: true labels
        y_pred_proba: predicted probabilities

    Returns:
        dict with evaluation metrics
    """

    auc = roc_auc_score(y_true, y_pred_proba)

    stats = {
        "auc": auc,
        "mean_predicted_proba": float(np.mean(y_pred_proba)),
        "std_predicted_proba": float(np.std(y_pred_proba)),
        "min_predicted_proba": float(np.min(y_pred_proba)),
        "max_predicted_proba": float(np.max(y_pred_proba)),
    }

    return stats