import pandas as pd

from src.utils.schema import DEFAULT_TARGET, P_DEFAULT


def find_optimal_threshold(df: pd.DataFrame, max_default_rate: float = 0.15):
    df = df.copy()

    if P_DEFAULT not in df.columns or DEFAULT_TARGET not in df.columns:
        raise ValueError(
            f"Required columns '{P_DEFAULT}' and/or '{DEFAULT_TARGET}' not found."
        )

    thresholds = sorted(df[P_DEFAULT].unique())

    best_threshold = None
    best_approval_rate = -1.0

    for t in thresholds:
        approved = df[df[P_DEFAULT] < t]

        if len(approved) == 0:
            continue

        approval_rate = len(approved) / len(df)
        default_rate = approved[DEFAULT_TARGET].mean()

        if default_rate <= max_default_rate and approval_rate > best_approval_rate:
            best_threshold = t
            best_approval_rate = approval_rate

    return best_threshold, best_approval_rate