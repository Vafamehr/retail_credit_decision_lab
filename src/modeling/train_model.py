import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.decision.approval_policy import apply_approval_policy
from src.evaluation.evaluate_model import evaluate_decisions
from src.evaluation.calibration import calibration_table, print_calibration

def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def prepare_data(df: pd.DataFrame):
    customer_ids = df["customer_id"].copy()
    y = df["default"]
    
    X = df.drop(columns=["default", "customer_id"])
    X = pd.get_dummies(X, drop_first=True)
    return X, y, customer_ids, df["default"].mean()


def train_model(X, y, customer_ids):
    X_train, X_test, y_train, y_test, _, id_test = train_test_split(
        X, y, customer_ids, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    predicted_risk = model.predict_proba(X_test_scaled)[:, 1]
    auc = roc_auc_score(y_test, predicted_risk)

    results = pd.DataFrame(
        {
            "customer_id": id_test.values,
            "actual_default": y_test.values,
            "predicted_risk": predicted_risk,
        }
    )

    results = apply_approval_policy(results)

    print(f"\nAUC: {auc:.4f}")

    evaluate_decisions(results)

    print("\n=== APPROVAL METRICS ===")

    approved = results[results["decision"] == "approve"]

    approval_rate = len(approved) / len(results)
    default_rate_approved = approved["actual_default"].mean()

    print(f"Approval Rate: {approval_rate:.2%}")
    print(f"Default Rate (Approved Only): {default_rate_approved:.2%}")


    calib = calibration_table(results, n_bins=5)
    print_calibration(calib)

    print("\n--- SAMPLE SCORES ---")
    print(results.head())

    return model, scaler, results


def main():
    path = "data/processed/loan_features.csv"
    df = load_data(path)
    X, y, customer_ids, mean_default= prepare_data(df)
    print(f"mean default is {mean_default}")
    train_model(X, y, customer_ids)


if __name__ == "__main__":
    main()