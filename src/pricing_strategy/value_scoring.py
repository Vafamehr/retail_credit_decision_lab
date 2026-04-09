import pandas as pd

from src.utils.config import LOSS_GIVEN_DEFAULT
from src.utils.schema import (
    ACCEPTED_OFFER,
    ADJUSTED_P_DEFAULT,
    EXPECTED_LOSS,
    EXPECTED_REVENUE,
    EXPECTED_VALUE,
    LOAN_AMOUNT,
    OFFERED_INTEREST_RATE,
    P_ACCEPT,
    RESPONSE_PROBABILITY,
)

FUNDING_COST = 0.03
SERVICING_COST = 0.015


def score_offers(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = [
        LOAN_AMOUNT,
        OFFERED_INTEREST_RATE,
        ADJUSTED_P_DEFAULT,
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for value scoring: {missing}")

    out = df.copy()

    if P_ACCEPT in out.columns:
        accept_prob = out[P_ACCEPT]
    elif RESPONSE_PROBABILITY in out.columns:
        accept_prob = out[RESPONSE_PROBABILITY]
        out[P_ACCEPT] = accept_prob
    elif ACCEPTED_OFFER in out.columns:
        accept_prob = out[ACCEPTED_OFFER].astype(float)
        out[P_ACCEPT] = accept_prob
    else:
        raise ValueError(
            f"Value scoring requires one of '{P_ACCEPT}', '{RESPONSE_PROBABILITY}', or '{ACCEPTED_OFFER}'."
        )

    gross_margin_rate = (
        out[OFFERED_INTEREST_RATE]* 2.0
        - FUNDING_COST
        - SERVICING_COST
    ).clip(lower=0.0)

    loss_severity = out[LOAN_AMOUNT] * LOSS_GIVEN_DEFAULT

    out[EXPECTED_REVENUE] = out[LOAN_AMOUNT] * gross_margin_rate

    out[EXPECTED_LOSS] = loss_severity

    out[EXPECTED_VALUE] = (
        accept_prob
        * (
            (1.0 - out[ADJUSTED_P_DEFAULT]) * out[EXPECTED_REVENUE]
            - out[ADJUSTED_P_DEFAULT] * out[EXPECTED_LOSS]
        )
    )

    return out