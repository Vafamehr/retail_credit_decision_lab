# src/credit_approval/train_model.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def prepare_data(df: pd.DataFrame):
    customer_ids = df["customer_id"].copy()
    y = df["default"]

    X = df.drop(columns=["default", "customer_id"])
    X = pd.get_dummies(X, drop_first=True)

    mean_default = df["default"].mean()

    return X, y, customer_ids, mean_default


def train_model(X, y, customer_ids):
    X_train, X_test, y_train, y_test, _, id_test = train_test_split(
        X,
        y,
        customer_ids,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    predicted_risk = model.predict_proba(X_test_scaled)[:, 1]

    return model, scaler, predicted_risk, y_test, id_test