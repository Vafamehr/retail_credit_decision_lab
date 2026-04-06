import pandas as pd

from src.utils.schema import DEFAULT_TARGET, P_DEFAULT


def calibration_table(df: pd.DataFrame, n_bins: int = 10) -> pd.DataFrame:
    df = df.copy()

    if P_DEFAULT not in df.columns or DEFAULT_TARGET not in df.columns:
        raise ValueError(
            f"Required columns '{P_DEFAULT}' and/or '{DEFAULT_TARGET}' not found."
        )

    df["bin"] = pd.qcut(df[P_DEFAULT], q=n_bins, duplicates="drop")

    calibration = (
        df.groupby("bin")
        .agg(
            avg_predicted_risk=(P_DEFAULT, "mean"),
            actual_default_rate=(DEFAULT_TARGET, "mean"),
            count=(DEFAULT_TARGET, "size"),
        )
        .reset_index()
    )

    return calibration


def print_calibration(calibration: pd.DataFrame):
    print("\n=== CALIBRATION TABLE ===")
    print(calibration)