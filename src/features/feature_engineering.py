import pandas as pd
from pathlib import Path


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["loan_to_income"] = df["loan_amount"] / (df["annual_income"] + 1e-6)

    if "credit_utilization" not in df.columns:
        df["credit_utilization"] = df["current_debt"] / (df["credit_limit"] + 1e-6)

    df["credit_score_bucket"] = pd.cut(
        df["credit_score"],
        bins=[300, 580, 670, 850],
        labels=["low", "medium", "high"],
    )

    df["high_utilization_flag"] = (df["credit_utilization"] > 0.7).astype(int)
    df["has_delinquency"] = (df["num_delinquencies"] > 0).astype(int)
    df["low_employment_years"] = (df["employment_years"] < 2).astype(int)
    df["dti_util_interaction"] = df["debt_to_income"] * df["credit_utilization"]
    df["loan_income_ratio"] = df["loan_amount"] / (df["annual_income"] + 1e-6)

    df["risky_profile_flag"] = (
        (df["credit_score"] < 650) & (df["debt_to_income"] > 0.4)
    ).astype(int)

    return df


def save_data(df: pd.DataFrame, path: str) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def main() -> None:
    input_path = "data/shared/synthetic_loan_data.csv"
    output_path = "data/shared/processed/loan_features.csv"

    df = load_data(input_path)
    df = build_features(df)
    save_data(df, output_path)

    print(f"Feature engineering complete. File saved to: {output_path}")
    print(f"Shape: {df.shape}")


if __name__ == "__main__":
    main()