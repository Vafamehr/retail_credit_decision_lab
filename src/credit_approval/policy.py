import pandas as pd


def apply_approval_policy(
    df: pd.DataFrame,
    approve_threshold: float,
    reject_threshold: float = 0.32
) -> pd.DataFrame:
    df = df.copy()

    df["decision"] = "review"

    df.loc[df["predicted_risk"] < approve_threshold, "decision"] = "approve"
    df.loc[df["predicted_risk"] >= reject_threshold, "decision"] = "reject"

    return df