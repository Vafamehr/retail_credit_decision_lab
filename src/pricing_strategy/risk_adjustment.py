import numpy as np
import pandas as pd

from src.utils.config import (
    BASELINE_INTEREST_RATE,
    BASELINE_PAYMENT_TO_INCOME_RATIO,
)
from src.utils.schema import (
    ADJUSTED_P_DEFAULT,
    BASE_P_DEFAULT,
    OFFERED_INTEREST_RATE,
    PAYMENT_TO_INCOME_RATIO,
)


def _safe_clip(prob: np.ndarray) -> np.ndarray:
    return np.clip(prob, 1e-6, 1 - 1e-6)


def apply_risk_adjustment(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = [
        BASE_P_DEFAULT,
        OFFERED_INTEREST_RATE,
        PAYMENT_TO_INCOME_RATIO,
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for risk adjustment: {missing}")

    out = df.copy()

    base_p = _safe_clip(out[BASE_P_DEFAULT].values)

    rate_diff = out[OFFERED_INTEREST_RATE].values - BASELINE_INTEREST_RATE
    pti_diff = (
        out[PAYMENT_TO_INCOME_RATIO].values
        - BASELINE_PAYMENT_TO_INCOME_RATIO
    )

    rate_effect = 0.55 * rate_diff

    # reward low APR with lower risk
    rate_effect = np.where(
        out[OFFERED_INTEREST_RATE].values < BASELINE_INTEREST_RATE,
        rate_effect * 0.7,
        rate_effect
    )

    adjusted_p = (
        base_p
        + rate_effect
        + 0.25 * pti_diff
    )

    adjusted_p = np.clip(adjusted_p, 0.01, 0.95)

    out[ADJUSTED_P_DEFAULT] = adjusted_p

    return out