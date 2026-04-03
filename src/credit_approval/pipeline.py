from src.modeling.train_model import load_data, prepare_data, train_model
from src.credit_approval.policy import apply_approval_policy
from src.evaluation.evaluate_model import evaluate_decisions
from src.evaluation.calibration import calibration_table, print_calibration

import pandas as pd
import os
import pickle

def run_credit_approval_pipeline():
    path = "data/processed/loan_features.csv"

    # Model identifier (for future extensibility)
    model_name = "logistic_regression"

    # Load + prepare
    df = load_data(path)
    X, y, customer_ids, mean_default = prepare_data(df)

    print("\n===== DATA SUMMARY =====")
    print(f"Mean default rate: {mean_default:.2%}")

    # Train + score
    model, scaler, predicted_risk, y_test, id_test = train_model(X, y, customer_ids)
    model_name = model.__class__.__name__.lower()
    scaler_name = scaler.__class__.__name__.lower()

    print("\n===== MODEL PERFORMANCE =====")

    
    # Save artifacts
    os.makedirs("artifacts", exist_ok=True)

    with open(f"artifacts/{model_name}_model.pkl", "wb") as f:
        pickle.dump(model, f)

    with open(f"artifacts/{scaler_name}_scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"Artifacts saved: {model_name}_model.pkl, {scaler_name}_scaler.pkl")

    # Build results
    results = pd.DataFrame({
        "customer_id": id_test.values,
        "actual_default": y_test.values,
        "predicted_risk": predicted_risk,
    })

    # Decision
    results = apply_approval_policy(results)

    # Evaluation
    evaluate_decisions(results)

    print("\n===== BUSINESS METRICS =====")
    approved = results[results["decision"] == "approve"]

    approval_rate = len(approved) / len(results)
    default_rate_approved = approved["actual_default"].mean()

    print(f"Approval Rate: {approval_rate:.2%}")
    print(f"Default Rate (Approved): {default_rate_approved:.2%}")

    print("\n===== CALIBRATION =====")
    calib = calibration_table(results, n_bins=5)
    print_calibration(calib)

    print("\n===== SAMPLE OUTPUT =====")
    print(results.head())


if __name__ == "__main__":
    run_credit_approval_pipeline()    
