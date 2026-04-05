# src/credit_approval/calibration.py

import pandas as pd


def calibration_table(df: pd.DataFrame, n_bins: int = 10) -> pd.DataFrame:
    df = df.copy()

    df["bin"] = pd.qcut(df["predicted_risk"], q=n_bins, duplicates="drop")

    calibration = df.groupby("bin").agg(
        avg_predicted_risk=("predicted_risk", "mean"),
        actual_default_rate=("actual_default", "mean"),
        count=("actual_default", "size"),
    ).reset_index()

    return calibration


def print_calibration(calibration: pd.DataFrame):
    print("\n=== CALIBRATION TABLE ===")
    print(calibration)