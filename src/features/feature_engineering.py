import pandas as pd

from src.utils.config import LOAN_FEATURES_PATH, SYNTHETIC_LOAN_DATA_PATH
from src.utils.schema import (
    AGE,
    ANNUAL_INCOME,
    BASE_INPUT_COLUMNS,
    CREDIT_SCORE,
    CREDIT_UTILIZATION,
    CUSTOMER_ID,
    DEBT_TO_INCOME,
    DELINQUENCY_COUNT,
    EMPLOYMENT_LENGTH_YEARS,
    ESTIMATED_MONTHLY_PAYMENT,
    EXISTING_CUSTOMER,
    INCOME_PER_MONTH,
    INQUIRY_COUNT,
    LOAN_AMOUNT,
    LOAN_TERM,
    LOAN_TO_INCOME_RATIO,
    NUM_EXISTING_PRODUCTS,
    PAYMENT_TO_INCOME_RATIO,
    RELATIONSHIP_TENURE_MONTHS,
    REVIEW_FLAG,
    RISK_SCORE_BAND,
    missing_columns,
)


def load_data(path) -> pd.DataFrame:
    return pd.read_csv(path)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    required_columns = missing_columns(df, BASE_INPUT_COLUMNS)
    if required_columns:
        raise ValueError(
            f"Missing required base input columns for feature engineering: {required_columns}"
        )

    df[INCOME_PER_MONTH] = df[ANNUAL_INCOME] / 12.0

    df[LOAN_TO_INCOME_RATIO] = df[LOAN_AMOUNT] / (df[ANNUAL_INCOME] + 1e-6)

    monthly_rate = 0.15 / 12.0
    n_periods = df[LOAN_TERM].clip(lower=1)

    df[ESTIMATED_MONTHLY_PAYMENT] = (
        df[LOAN_AMOUNT]
        * (
            monthly_rate * (1 + monthly_rate) ** n_periods
        )
        / (
            ((1 + monthly_rate) ** n_periods) - 1 + 1e-6
        )
    )

    df[PAYMENT_TO_INCOME_RATIO] = (
        df[ESTIMATED_MONTHLY_PAYMENT] / (df[INCOME_PER_MONTH] + 1e-6)
    )

    df[RISK_SCORE_BAND] = pd.cut(
        df[CREDIT_SCORE],
        bins=[300, 580, 670, 740, 850],
        labels=["poor", "fair", "good", "excellent"],
        include_lowest=True,
    ).astype(str)

    df[REVIEW_FLAG] = (
        (df[CREDIT_SCORE] < 620)
        | (df[DEBT_TO_INCOME] > 0.45)
        | (df[CREDIT_UTILIZATION] > 0.80)
        | (df[DELINQUENCY_COUNT] > 0)
    ).astype(int)

    return df


def save_data(df: pd.DataFrame, path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def main() -> None:
    df = load_data(SYNTHETIC_LOAN_DATA_PATH)
    df = build_features(df)
    save_data(df, LOAN_FEATURES_PATH)

    print(f"Feature engineering complete. File saved to: {LOAN_FEATURES_PATH}")
    print(f"Shape: {df.shape}")


if __name__ == "__main__":
    main()