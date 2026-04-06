import numpy as np
import pandas as pd

from src.utils.config import SYNTHETIC_LOAN_DATA_PATH, ensure_directories
from src.utils.schema import (
    AGE,
    ANNUAL_INCOME,
    CREDIT_SCORE,
    CREDIT_UTILIZATION,
    CUSTOMER_ID,
    DEBT_TO_INCOME,
    DEFAULT_TARGET,
    DELINQUENCY_COUNT,
    EMPLOYMENT_LENGTH_YEARS,
    EXISTING_CUSTOMER,
    INQUIRY_COUNT,
    LOAN_AMOUNT,
    LOAN_TERM,
    NUM_EXISTING_PRODUCTS,
    RELATIONSHIP_TENURE_MONTHS,
)


def generate_synthetic_loan_data(n: int = 10000, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    data = pd.DataFrame()

    data[CUSTOMER_ID] = np.arange(1, n + 1)

    data[ANNUAL_INCOME] = rng.normal(75000, 30000, n).clip(20000, 200000)
    data[CREDIT_SCORE] = rng.normal(680, 70, n).clip(300, 850)
    data[LOAN_AMOUNT] = rng.normal(20000, 10000, n).clip(1000, 50000)
    data[LOAN_TERM] = rng.choice([36, 60], size=n, p=[0.65, 0.35])

    data[AGE] = rng.normal(42, 12, n).clip(21, 75).round().astype(int)
    data[EMPLOYMENT_LENGTH_YEARS] = rng.integers(0, 21, n)

    data[DEBT_TO_INCOME] = rng.beta(2, 5, n).clip(0.01, 0.95)
    data[CREDIT_UTILIZATION] = rng.beta(2.2, 2.0, n).clip(0.01, 0.99)
    data[DELINQUENCY_COUNT] = rng.poisson(0.5, n)
    data[INQUIRY_COUNT] = rng.poisson(1.2, n)

    existing_customer = rng.binomial(1, 0.45, n)
    relationship_tenure = np.where(
        existing_customer == 1,
        rng.integers(6, 121, n),
        0,
    )
    existing_products = np.where(
        existing_customer == 1,
        rng.integers(1, 5, n),
        0,
    )

    data[EXISTING_CUSTOMER] = existing_customer.astype(int)
    data[RELATIONSHIP_TENURE_MONTHS] = relationship_tenure.astype(int)
    data[NUM_EXISTING_PRODUCTS] = existing_products.astype(int)

    risk_score = (
        -2.25
        + (700 - data[CREDIT_SCORE]) * 0.0027
        + data[DEBT_TO_INCOME] * 1.35
        + data[CREDIT_UTILIZATION] * 1.10
        + data[DELINQUENCY_COUNT] * 0.38
        + data[INQUIRY_COUNT] * 0.10
        - data[EMPLOYMENT_LENGTH_YEARS] * 0.02
        - data[EXISTING_CUSTOMER] * 0.18
        - data[NUM_EXISTING_PRODUCTS] * 0.04
        + 1.60 * (data[DEBT_TO_INCOME] * data[CREDIT_UTILIZATION])
        + 1.00 * (data[CREDIT_SCORE] < 600).astype(int)
        + 1.10
        * (
            (data[CREDIT_UTILIZATION] > 0.80)
            & (data[DEBT_TO_INCOME] > 0.50)
        ).astype(int)
        + 0.45 * (data[DELINQUENCY_COUNT] >= 2).astype(int)
    )

    probability_default = 1.0 / (1.0 + np.exp(-risk_score))
    data[DEFAULT_TARGET] = rng.binomial(1, probability_default)

    return data


def main() -> None:
    ensure_directories()

    df = generate_synthetic_loan_data()
    SYNTHETIC_LOAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SYNTHETIC_LOAN_DATA_PATH, index=False)

    print(f"Data generated and saved to: {SYNTHETIC_LOAN_DATA_PATH}")
    print(f"Shape: {df.shape}")
    print(f"Default rate: {df[DEFAULT_TARGET].mean():.2%}")


if __name__ == "__main__":
    main()