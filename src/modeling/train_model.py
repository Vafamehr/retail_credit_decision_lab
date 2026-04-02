import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def prepare_data(df: pd.DataFrame):
    y = df["default"]
    X = df.drop(columns=["default", "customer_id"])
    X = pd.get_dummies(X, drop_first=True)
    return X, y


def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    # Model prediction: probability of default
    predicted_risk = model.predict_proba(X_test_scaled)[:, 1]

    # Ground truth: what actually happened (0 = no default, 1 = default)
    true_default = y_test.values

    auc = roc_auc_score(y_test, predicted_risk)
    print(f"\nAUC: {auc:.4f}")

    # Overall default fraction across ALL test rows (baseline reality)
    print(f"Overall Default Fraction (all test rows): {true_default.mean():.2%}")

    thresholds = [0.3, 0.5, 0.7]

    for t in thresholds:
        # Select rows where predicted risk is below threshold
        selected = predicted_risk < t

        selected_count = selected.sum()
        total_count = len(selected)

        print("\n------------------------------")
        print(f"Threshold: {t:.2f}")

        # Fraction of rows selected by this threshold
        print(f"Selected Fraction: {selected_count}/{total_count} = {selected_count/total_count:.2%}")

        if selected_count > 0:
            # Average predicted default probability for selected rows
            selected_predicted_fraction = predicted_risk[selected].mean()

            # Actual default rate (truth) for the same selected rows
            selected_true_fraction = true_default[selected].mean()

            print(
                f"Predicted Default Fraction (selected rows): "
                f"{selected_predicted_fraction:.2%}"
            )
            print(
                f"True Default Fraction (selected rows): "
                f"{selected_true_fraction:.2%}"
            )
        else:
            print("No rows selected")

    return model

def main():
    path = "data/processed/loan_features.csv"
    df = load_data(path)
    X, y = prepare_data(df)
    train_model(X, y)


if __name__ == "__main__":
    main()