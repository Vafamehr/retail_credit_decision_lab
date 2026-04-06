import pandas as pd

from src.utils.schema import P_DEFAULT


def apply_approval_policy(
    df: pd.DataFrame,
    approve_threshold: float,
    reject_threshold: float = 0.32,
) -> pd.DataFrame:
    df = df.copy()

    if P_DEFAULT not in df.columns:
        raise ValueError(f"Required column '{P_DEFAULT}' not found in input DataFrame.")

    df["decision"] = "review"

    df.loc[df[P_DEFAULT] < approve_threshold, "decision"] = "approve"
    df.loc[df[P_DEFAULT] >= reject_threshold, "decision"] = "reject"

    return df