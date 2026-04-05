from pathlib import Path
import pandas as pd
import joblib

from src.credit_approval.train_model import load_data, prepare_data, train_model
from src.credit_approval.policy import apply_approval_policy
from src.credit_approval.evaluate_model import evaluate_decisions
from src.credit_approval.calibration import calibration_table, print_calibration
from src.credit_approval.optimize_thresholds import find_optimal_threshold





def save_artifacts(model, scaler, feature_columns):
    output_dir = Path("artifacts/credit_approval")
    output_dir.mkdir(parents=True, exist_ok=True)

    model_name = model.__class__.__name__.lower()
    scaler_name = scaler.__class__.__name__.lower()

    model_path = output_dir / f"{model_name}_model.pkl"
    scaler_path = output_dir / f"{scaler_name}_scaler.pkl"
    feature_path = output_dir / "credit_feature_columns.pkl"

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(feature_columns, feature_path)

    print(f"Artifacts saved to: {output_dir}")   


def run_credit_approval_pipeline():
    path = "data/shared/processed/loan_features.csv"

    df = load_data(path)
    X, y, customer_ids, mean_default = prepare_data(df)

    print("\n===== CREDIT APPROVAL DATA SUMMARY =====")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print(f"Feature Count After Encoding: {X.shape[1]}")
    print(f"Mean Default Rate: {mean_default:.2%}")

    model, scaler, predicted_risk, y_test, id_test = train_model(X, y, customer_ids)    
    save_artifacts(model, scaler, X.columns.tolist())

    results = pd.DataFrame({
        "customer_id": id_test.values,
        "actual_default": y_test.values,
        "predicted_risk": predicted_risk,
    })

    threshold, optimized_approval_rate = find_optimal_threshold(
        results,
        max_default_rate=0.15
    )

    print("\n===== THRESHOLD OPTIMIZATION =====")
    print(f"Optimized approval threshold: {threshold:.4f}")
    print(f"Optimized approval rate: {optimized_approval_rate:.2%}")
    print("Constraint: approved default rate <= 15.00%")

    results = apply_approval_policy(
        results,
        approve_threshold=threshold,
        reject_threshold=0.32
    )

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