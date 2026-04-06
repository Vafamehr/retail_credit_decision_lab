import joblib

from src.response_modeling.data_prep import (
    build_response_modeling_dataset,
    prepare_model_inputs,
)
from src.response_modeling.evaluate_response_model import evaluate_response_model
from src.response_modeling.train_response_model import train_response_model
from src.utils.config import (
    LOAN_FEATURES_PATH,
    RESPONSE_FEATURE_COLUMNS_PATH,
    RESPONSE_MODEL_PATH,
    RESPONSE_MODELING_FEATURES_PATH,
    RESPONSE_SCALER_PATH,
    ensure_directories,
)
from src.utils.schema import ACCEPTED_OFFER, OFFER_NAME


def save_artifacts(model, scaler, feature_columns) -> None:
    RESPONSE_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, RESPONSE_MODEL_PATH)
    joblib.dump(scaler, RESPONSE_SCALER_PATH)
    joblib.dump(feature_columns, RESPONSE_FEATURE_COLUMNS_PATH)

    print(f"Model saved to: {RESPONSE_MODEL_PATH}")
    print(f"Scaler saved to: {RESPONSE_SCALER_PATH}")
    print(f"Feature columns saved to: {RESPONSE_FEATURE_COLUMNS_PATH}")


def run_response_modeling_pipeline(random_state: int = 42):
    ensure_directories()

    df = build_response_modeling_dataset(
        input_path=LOAN_FEATURES_PATH,
        output_path=RESPONSE_MODELING_FEATURES_PATH,
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

    print("\n===== ACCEPTANCE RATE BY OFFER =====")
    print(df.groupby(OFFER_NAME)[ACCEPTED_OFFER].mean().to_string())

    return {
        "model": model,
        "scaler": scaler,
        "feature_columns": X.columns.tolist(),
        "metrics": metrics,
        "y_test": y_test,
        "predicted_proba": predicted_proba,
        "id_test": id_test,
        "dataset_shape": df.shape,
        "model_input_shape": X.shape,
    }


if __name__ == "__main__":
    run_response_modeling_pipeline()