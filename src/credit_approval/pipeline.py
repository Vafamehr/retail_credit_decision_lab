import joblib
import pandas as pd

from src.credit_approval.calibration import calibration_table, print_calibration
from src.credit_approval.evaluate_model import evaluate_decisions
from src.credit_approval.optimize_thresholds import find_optimal_threshold
from src.credit_approval.policy import apply_approval_policy
from src.credit_approval.train_model import load_data, prepare_data, train_model
from src.utils.config import (
    CREDIT_FEATURE_COLUMNS_PATH,
    CREDIT_MODEL_PATH,
    CREDIT_SCALER_PATH,
    DEFAULT_APPROVAL_THRESHOLD,
    LOAN_FEATURES_PATH,
    ensure_directories,
)
from src.utils.schema import CUSTOMER_ID, DEFAULT_TARGET, P_DEFAULT


def save_artifacts(model, scaler, feature_columns) -> None:
    CREDIT_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, CREDIT_MODEL_PATH)
    joblib.dump(scaler, CREDIT_SCALER_PATH)
    joblib.dump(feature_columns, CREDIT_FEATURE_COLUMNS_PATH)

    print(f"Model saved to: {CREDIT_MODEL_PATH}")
    print(f"Scaler saved to: {CREDIT_SCALER_PATH}")
    print(f"Feature columns saved to: {CREDIT_FEATURE_COLUMNS_PATH}")


def run_credit_approval_pipeline():
    ensure_directories()

    df = load_data(LOAN_FEATURES_PATH)
    X, y, customer_ids, mean_default = prepare_data(df)

    print("\n===== CREDIT APPROVAL DATA SUMMARY =====")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Feature Count After Encoding: {X.shape[1]}")
    print(f"Mean Default Rate: {mean_default:.2%}")

    model, scaler, predicted_risk, y_test, id_test = train_model(X, y, customer_ids)
    save_artifacts(model, scaler, X.columns.tolist())

    results = pd.DataFrame(
        {
            CUSTOMER_ID: id_test.values,
            DEFAULT_TARGET: y_test.values,
            P_DEFAULT: predicted_risk,
        }
    )

    threshold, optimized_approval_rate = find_optimal_threshold(
        results,
        max_default_rate=0.15,
    )

    print("\n===== THRESHOLD OPTIMIZATION =====")
    print(f"Optimized approval threshold: {threshold:.4f}")
    print(f"Optimized approval rate: {optimized_approval_rate:.2%}")
    print("Constraint: approved default rate <= 15.00%")

    results = apply_approval_policy(
        results,
        approve_threshold=threshold,
        reject_threshold=max(DEFAULT_APPROVAL_THRESHOLD, 0.32),
    )

    evaluate_decisions(results)

    print("\n===== BUSINESS METRICS =====")
    approved = results[results["decision"] == "approve"]

    approval_rate = len(approved) / len(results)
    default_rate_approved = approved[DEFAULT_TARGET].mean()

    print(f"Approval Rate: {approval_rate:.2%}")
    print(f"Default Rate (Approved): {default_rate_approved:.2%}")

    print("\n===== CALIBRATION =====")
    calib = calibration_table(results, n_bins=5)
    print_calibration(calib)

    print("\n===== SAMPLE OUTPUT =====")
    print(results.head())

    return {
        "model": model,
        "scaler": scaler,
        "results": results,
        "calibration": calib,
        "approval_threshold": threshold,
        "approval_rate": approval_rate,
        "approved_default_rate": default_rate_approved,
        "dataset_shape": df.shape,
        "model_input_shape": X.shape,
    }


if __name__ == "__main__":
    run_credit_approval_pipeline()