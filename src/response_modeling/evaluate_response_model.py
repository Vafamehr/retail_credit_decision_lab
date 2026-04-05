# src/response_modeling/evaluate_response_model.py

from sklearn.metrics import roc_auc_score
import numpy as np
import pandas as pd


def evaluate_response_model(y_true, y_pred_proba):
    """
    Evaluate response model performance.

    Returns:
        dict with:
        - auc
        - prediction stats
        - calibration gap
        - decile lift table
    """

    y_true = np.array(y_true)
    y_pred_proba = np.array(y_pred_proba)

    # Core metric
    auc = roc_auc_score(y_true, y_pred_proba)

    # Basic stats
    mean_pred = float(np.mean(y_pred_proba))
    actual_rate = float(np.mean(y_true))

    stats = {
        "auc": auc,
        "mean_predicted_proba": mean_pred,
        "actual_response_rate": actual_rate,
        "calibration_gap": float(mean_pred - actual_rate),
        "std_predicted_proba": float(np.std(y_pred_proba)),
        "min_predicted_proba": float(np.min(y_pred_proba)),
        "max_predicted_proba": float(np.max(y_pred_proba)),
    }

    # Decile analysis (business-friendly)
    df = pd.DataFrame({
        "y_true": y_true,
        "y_pred": y_pred_proba
    })

    df["decile"] = pd.qcut(df["y_pred"], 10, labels=False, duplicates="drop")

    decile_table = (
        df.groupby("decile")
        .agg(
            count=("y_true", "size"),
            avg_pred=("y_pred", "mean"),
            actual_rate=("y_true", "mean"),
        )
        .sort_index(ascending=False)
        .reset_index()
    )

    stats["decile_table"] = decile_table

    return stats