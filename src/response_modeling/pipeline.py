# src/response_modeling/pipeline.py

from pathlib import Path

import numpy as np
import pandas as pd
import joblib

from src.response_modeling.train_response_model import train_response_model
from src.response_modeling.evaluate_response_model import evaluate_response_model


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def load_base_data(input_path: str | Path) -> pd.DataFrame:
    return pd.read_csv(input_path).copy()


def add_offer_features(df: pd.DataFrame, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    out = df.copy()

    credit_score = out["credit_score"].clip(300, 850)
    debt_to_income = out["debt_to_income"].clip(0.0, 1.0)
    loan_amount = out["loan_amount"].clip(lower=1000)
    annual_income = out["annual_income"].clip(lower=10000)
    term = out["loan_term"].clip(lower=12)

    base_rate = (
        0.20
        - 0.00012 * (credit_score - 650)
        + 0.05 * debt_to_income
        + 0.0000010 * loan_amount
        + 0.03 * out["high_utilization_flag"]
        + 0.02 * out["has_delinquency"]
        + 0.01 * out["risky_profile_flag"]
    )

    rate_noise = rng.normal(0.0, 0.02, len(out))
    offered_interest_rate = np.clip(base_rate + rate_noise, 0.06, 0.32)

    monthly_rate = offered_interest_rate / 12.0
    monthly_payment = (
        loan_amount
        * monthly_rate
        * (1 + monthly_rate) ** term
        / (((1 + monthly_rate) ** term) - 1)
    )

    monthly_payment = np.where(
        np.isfinite(monthly_payment),
        monthly_payment,
        loan_amount / term,
    )

    out["offered_interest_rate"] = np.round(offered_interest_rate, 4)
    out["estimated_monthly_payment"] = np.round(monthly_payment, 2)
    out["payment_to_income_ratio"] = np.round(
        monthly_payment / (annual_income / 12.0), 4
    )

    return out


def add_relationship_features(df: pd.DataFrame, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    out = df.copy()

    existing_customer = rng.binomial(1, 0.45, len(out))
    relationship_tenure_months = np.where(
        existing_customer == 1,
        rng.integers(6, 121, len(out)),
        0,
    )
    num_existing_products = np.where(
        existing_customer == 1,
        rng.integers(1, 5, len(out)),
        0,
    )

    out["existing_customer"] = existing_customer.astype(int)
    out["relationship_tenure_months"] = relationship_tenure_months.astype(int)
    out["num_existing_products"] = num_existing_products.astype(int)

    return out


def simulate_acceptance(df: pd.DataFrame, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    out = df.copy()

    review_flag = (
        (out["credit_score"] < 640)
        | (out["debt_to_income"] > 0.43)
        | (out["num_delinquencies"] >= 2)
        | (out["high_utilization_flag"] == 1)
    ).astype(int)
    out["review_flag"] = review_flag

    purpose = out["loan_purpose"].astype(str).str.lower()

    purpose_bonus = np.select(
        [
            purpose.eq("debt_consolidation"),
            purpose.eq("home_improvement"),
            purpose.eq("major_purchase"),
        ],
        [0.12, 0.06, 0.03],
        default=0.0,
    )

    segment_noise = rng.normal(0.0, 0.60, len(out))

    score = (
        -0.10
        + 0.0035 * (out["credit_score"] - 650)
        + 0.000006 * (out["annual_income"] - 70000)
        - 3.00 * out["payment_to_income_ratio"]
        - 2.00 * out["offered_interest_rate"]
        - 1.10 * out["debt_to_income"]
        - 0.15 * out["num_delinquencies"]
        - 0.000004 * out["loan_amount"]
        + 0.25 * out["existing_customer"]
        + 0.0012 * out["relationship_tenure_months"]
        + 0.06 * out["num_existing_products"]
        - 0.20 * out["review_flag"]
        + purpose_bonus
        + segment_noise
    )

    response_probability = sigmoid(score)
    accepted_offer = rng.binomial(1, response_probability)

    out["response_probability"] = np.round(response_probability, 4)
    out["accepted_offer"] = accepted_offer.astype(int)

    return out


def build_response_modeling_dataset(
    input_path: str | Path = "data/shared/processed/loan_features.csv",
    output_path: str | Path = "data/response_modeling/processed/response_modeling_features.csv",
    random_state: int = 42,
) -> pd.DataFrame:
    df = load_base_data(input_path)
    df = add_offer_features(df, random_state=random_state)
    df = add_relationship_features(df, random_state=random_state)
    df = simulate_acceptance(df, random_state=random_state)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    return df


def prepare_model_inputs(df: pd.DataFrame):
    target = "accepted_offer"

    drop_cols = [
        "accepted_offer",
        "response_probability",
    ]

    X = df.drop(columns=[c for c in drop_cols if c in df.columns])
    y = df[target]
    ids = df.index.to_series(name="row_id")

    X = pd.get_dummies(X, drop_first=True)

    return X, y, ids


def save_artifacts(model, scaler, feature_columns):
    output_dir = Path("artifacts/response_modeling")
    output_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, output_dir / "response_model.pkl")
    joblib.dump(scaler, output_dir / "response_scaler.pkl")
    joblib.dump(feature_columns, output_dir / "response_feature_columns.pkl")


def run_response_modeling_pipeline(
    input_path: str | Path = "data/shared/processed/loan_features.csv",
    output_path: str | Path = "data/response_modeling/processed/response_modeling_features.csv",
    random_state: int = 42,
):
    df = build_response_modeling_dataset(
        input_path=input_path,
        output_path=output_path,
        random_state=random_state,
    )

    X, y, ids = prepare_model_inputs(df)

    model, scaler, predicted_proba, y_test, id_test = train_response_model(X, y, ids)

    metrics = evaluate_response_model(y_test, predicted_proba)

    save_artifacts(model, scaler, X.columns.tolist())

    print("\n===== RESPONSE MODELING DATA SUMMARY =====")
    print(f"Rows: {len(df)}")
    print(f"Columns: {df.shape[1]}")
    print(f"Acceptance Rate: {y.mean():.2%}")
    print(f"Feature Count After Encoding: {X.shape[1]}")

    print("\n===== RESPONSE MODEL PERFORMANCE =====")
    print(f"AUC: {metrics['auc']:.4f}")
    print(f"Predicted Probability Mean: {metrics['mean_predicted_proba']:.4f}")
    print(f"Actual Response Rate: {metrics['actual_response_rate']:.4f}")
    print(f"Calibration Gap: {metrics['calibration_gap']:.4f}")
    print(f"Predicted Probability Std: {metrics['std_predicted_proba']:.4f}")
    print(f"Min Probability: {metrics['min_predicted_proba']:.4f}")
    print(f"Max Probability: {metrics['max_predicted_proba']:.4f}")

    print("\n===== RESPONSE DECILE TABLE =====")
    print(metrics["decile_table"])

    return {
        "model": model,
        "scaler": scaler,
        "feature_columns": X.columns.tolist(),
        "metrics": metrics,
        "y_test": y_test,
        "predicted_proba": predicted_proba,
        "id_test": id_test,
        "dataset_path": str(output_path),
        "dataset_shape": df.shape,
        "model_input_shape": X.shape,
    }


if __name__ == "__main__":
    run_response_modeling_pipeline()