# src/response_modeling/pipeline.py

import os
import pickle
import pandas as pd

from src.response_modeling.train_response_model import train_response_model
from src.response_modeling.evaluate_response_model import evaluate_response_model


def load_data(path: str):
    df = pd.read_csv(path)
    return df


def prepare_data(df: pd.DataFrame):
    """
    Prepare features for response modeling.

    Assumptions:
    - 'response' is target (1 = responded, 0 = not)
    - 'customer_id' exists
    """

    df = df.copy()

    y = df["response"]
    ids = df["customer_id"]

    X = df.drop(columns=["response", "customer_id"])

    return X, y, ids


def run_response_modeling_pipeline():
    path = "data/processed/response_modeling_features.csv"

    # Load + prepare
    df = load_data(path)
    X, y, ids = prepare_data(df)

    print("\n===== DATA SUMMARY =====")
    print(f"Response rate: {y.mean():.2%}")

    # Train
    model, scaler, predicted_proba, y_test, id_test = train_response_model(
        X, y, ids
    )

    # Save artifacts
    os.makedirs("artifacts/response_modeling", exist_ok=True)

    with open("artifacts/response_modeling/model.pkl", "wb") as f:
        pickle.dump(model, f)

    with open("artifacts/response_modeling/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    # Evaluate
    metrics = evaluate_response_model(y_test, predicted_proba)

    print("\n===== MODEL PERFORMANCE =====")
    print(f"AUC: {metrics['auc']:.4f}")
    print(f"Predicted Probability Mean: {metrics['mean_predicted_proba']:.4f}")
    print(f"Predicted Probability Std: {metrics['std_predicted_proba']:.4f}")
    print(f"Min Probability: {metrics['min_predicted_proba']:.4f}")
    print(f"Max Probability: {metrics['max_predicted_proba']:.4f}")

    return {
        "model": model,
        "scaler": scaler,
        "metrics": metrics,
        "y_test": y_test,
        "predicted_proba": predicted_proba,
        "id_test": id_test,
    }


if __name__ == "__main__":
    run_response_modeling_pipeline()