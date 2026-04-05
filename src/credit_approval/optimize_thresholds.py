import pandas as pd


def find_optimal_threshold(df: pd.DataFrame, max_default_rate: float = 0.15):
    df = df.copy()

    thresholds = sorted(df["predicted_risk"].unique())

    best_threshold = None
    best_approval_rate = -1.0

    for t in thresholds:
        approved = df[df["predicted_risk"] < t]

        if len(approved) == 0:
            continue

        approval_rate = len(approved) / len(df)
        default_rate = approved["actual_default"].mean()

        if default_rate <= max_default_rate and approval_rate > best_approval_rate:
            best_threshold = t
            best_approval_rate = approval_rate

    return best_threshold, best_approval_rate