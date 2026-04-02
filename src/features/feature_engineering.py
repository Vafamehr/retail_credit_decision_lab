import os
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1. Loan to income ratio
    df["loan_to_income"] = df["loan_amount"] / (df["annual_income"] + 1e-6)

    # 2. Credit utilization
    if "credit_utilization" not in df.columns:
        df["credit_utilization"] = df["current_debt"] / (df["credit_limit"] + 1e-6)

    # 3. Credit score buckets
    df["credit_score_bucket"] = pd.cut(
        df["credit_score"],
        bins=[300, 580, 670, 850],
        labels=["low", "medium", "high"]
    )

    # 4. High utilization flag
    df["high_utilization_flag"] = (df["credit_utilization"] > 0.7).astype(int)

    # 5. Any delinquency flag
    df["has_delinquency"] = (df["num_delinquencies"] > 0).astype(int)

    # 6. Employment stability
    df["low_employment_years"] = (df["employment_years"] < 2).astype(int)

    return df


def save_data(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


def main() -> None:
    input_path = "data/synthetic_loan_data.csv"
    output_path = "data/processed/loan_features.csv"

    df = load_data(input_path)
    df = build_features(df)
    save_data(df, output_path)

    print(f"Feature engineering complete. File saved to: {output_path}")

    print("\n--- DATA CHECK ---")
    print(df.head())

    print("\n--- NULLS ---")
    print(df.isna().sum())

    print("\n--- SUMMARY ---")
    print(df.describe())


if __name__ == "__main__":
    main()