import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1. Loan to income ratio
    df["loan_to_income"] = df["loan_amount"] / df["annual_income"]

    # 2. Credit score buckets
    df["credit_score_bucket"] = pd.cut(
        df["credit_score"],
        bins=[300, 580, 670, 850],
        labels=["low", "medium", "high"]
    )

    # 3. High utilization flag
    df["high_utilization_flag"] = (df["credit_utilization"] > 0.7).astype(int)

    # 4. Any delinquency flag
    df["has_delinquency"] = (df["num_delinquencies"] > 0).astype(int)

    # 5. Employment stability
    df["low_employment_years"] = (df["employment_years"] < 2).astype(int)

    return df