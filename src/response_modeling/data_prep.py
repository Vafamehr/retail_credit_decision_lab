from pathlib import Path

import numpy as np
import pandas as pd

from src.utils.config import APR_OPTIONS
from src.utils.schema import (
    ACCEPTED_OFFER,
    CUSTOMER_ID,
    ESTIMATED_MONTHLY_PAYMENT,
    OFFER_NAME,
    OFFERED_INTEREST_RATE,
    PAYMENT_TO_INCOME_RATIO,
    RESPONSE_MODELING_FEATURE_COLUMNS,
    RESPONSE_PROBABILITY,
    missing_columns,
)


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def load_base_data(input_path: Path) -> pd.DataFrame:
    return pd.read_csv(input_path).copy()


def calculate_monthly_payment(
    loan_amount: pd.Series,
    annual_interest_rate: pd.Series,
    term_months: pd.Series,
) -> pd.Series:
    loan_amount = loan_amount.astype(float)
    annual_interest_rate = annual_interest_rate.astype(float)
    term_months = term_months.astype(float)

    monthly_rate = annual_interest_rate / 12.0

    payment = np.where(
        monthly_rate == 0,
        loan_amount / term_months,
        loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** (-term_months)),
    )

    return pd.Series(payment, index=loan_amount.index)


def expand_customer_offer_rows(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = [
        CUSTOMER_ID,
        "annual_income",
        "loan_amount",
        "loan_term",
    ]
    missing = missing_columns(df, required_columns)
    if missing:
        raise ValueError(
            f"Missing required columns for response offer expansion: {missing}"
        )

    offer_frames = []

    for offer_name, apr in APR_OPTIONS.items():
        temp = df.copy()
        temp[OFFER_NAME] = offer_name
        temp[OFFERED_INTEREST_RATE] = apr
        offer_frames.append(temp)

    out = pd.concat(offer_frames, ignore_index=True)

    monthly_income = out["annual_income"] / 12.0

    out[ESTIMATED_MONTHLY_PAYMENT] = calculate_monthly_payment(
        loan_amount=out["loan_amount"],
        annual_interest_rate=out[OFFERED_INTEREST_RATE],
        term_months=out["loan_term"],
    )

    out[PAYMENT_TO_INCOME_RATIO] = (
        out[ESTIMATED_MONTHLY_PAYMENT] / (monthly_income + 1e-6)
    )

    return out


def simulate_acceptance(df: pd.DataFrame, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    out = df.copy()

    score = (
        -0.15
        + 0.0028 * (out["credit_score"] - 650)
        - 5.50 * out[PAYMENT_TO_INCOME_RATIO]
        - 6.00 * out[OFFERED_INTEREST_RATE]
        - 1.30 * out["debt_to_income"]
        - 0.18 * out["delinquency_count"]
        - 0.0000025 * out["loan_amount"]
        + 0.30 * out["existing_customer"]
        + 0.0015 * out["relationship_tenure_months"]
        + 0.08 * out["num_existing_products"]
        - 0.30 * out["review_flag"]
    )

    probs = sigmoid(score)
    accepted = rng.binomial(1, probs)

    out[RESPONSE_PROBABILITY] = np.round(probs, 4)
    out[ACCEPTED_OFFER] = accepted.astype(int)

    return out


def build_response_modeling_dataset(
    input_path: Path,
    output_path: Path,
    random_state: int = 42,
) -> pd.DataFrame:
    df = load_base_data(input_path)
    df = expand_customer_offer_rows(df)
    df = simulate_acceptance(df, random_state=random_state)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    return df


def prepare_model_inputs(df: pd.DataFrame):
    required_columns = [CUSTOMER_ID, ACCEPTED_OFFER] + RESPONSE_MODELING_FEATURE_COLUMNS
    missing = missing_columns(df, required_columns)
    if missing:
        raise ValueError(
            f"Missing required columns for response model inputs: {missing}"
        )

    X = df[RESPONSE_MODELING_FEATURE_COLUMNS].copy()
    y = df[ACCEPTED_OFFER].copy()
    ids = df[CUSTOMER_ID].copy()

    X = pd.get_dummies(X, drop_first=True)

    return X, y, ids