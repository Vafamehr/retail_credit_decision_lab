import numpy as np
import pandas as pd
from pathlib import Path


def generate_synthetic_loan_data(n=10000, random_state=42):
    np.random.seed(random_state)

    data = pd.DataFrame()

    data["customer_id"] = np.arange(1, n + 1)
    data["annual_income"] = np.random.normal(75000, 30000, n).clip(20000, 200000)
    data["credit_score"] = np.random.normal(680, 70, n).clip(300, 850)
    data["loan_amount"] = np.random.normal(20000, 10000, n).clip(1000, 50000)
    data["loan_term"] = np.random.choice([36, 60], size=n)
    data["debt_to_income"] = np.random.beta(2, 5, n)
    data["employment_years"] = np.random.randint(0, 20, n)
    data["num_delinquencies"] = np.random.poisson(0.5, n)
    data["credit_utilization"] = np.random.beta(2, 2, n)
    data["num_accounts"] = np.random.randint(1, 15, n)

    data["home_ownership"] = np.random.choice(
        ["RENT", "OWN", "MORTGAGE"], size=n, p=[0.4, 0.2, 0.4]
    )

    data["loan_purpose"] = np.random.choice(
        ["debt_consolidation", "credit_card", "home_improvement", "other"], size=n
    )

    risk_score = (
        -2.2
        + (700 - data["credit_score"]) * 0.0025
        + data["debt_to_income"] * 1.2
        + data["credit_utilization"] * 1.0
        + data["num_delinquencies"] * 0.35
        - data["employment_years"] * 0.015
        + 1.5 * (data["debt_to_income"] * data["credit_utilization"])
        + 1.0 * (data["credit_score"] < 600)
        + 1.2 * ((data["credit_utilization"] > 0.8) & (data["debt_to_income"] > 0.5))
    )

    probability_default = 1 / (1 + np.exp(-risk_score))
    data["default"] = np.random.binomial(1, probability_default)

    return data


if __name__ == "__main__":
    df = generate_synthetic_loan_data()

    output_path = Path("data/shared/synthetic_loan_data.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"Data generated and saved to: {output_path}")
    print(f"Shape: {df.shape}")