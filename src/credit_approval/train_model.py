import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.utils.schema import (
    CREDIT_APPROVAL_FEATURE_COLUMNS,
    CUSTOMER_ID,
    DEFAULT_TARGET,
    missing_columns,
)


def load_data(path) -> pd.DataFrame:
    return pd.read_csv(path)


def prepare_data(df: pd.DataFrame):
    required_columns = [CUSTOMER_ID, DEFAULT_TARGET] + CREDIT_APPROVAL_FEATURE_COLUMNS
    missing = missing_columns(df, required_columns)
    if missing:
        raise ValueError(
            f"Missing required columns for credit approval training: {missing}"
        )

    customer_ids = df[CUSTOMER_ID].copy()
    y = df[DEFAULT_TARGET].copy()

    X = df[CREDIT_APPROVAL_FEATURE_COLUMNS].copy()
    X = pd.get_dummies(X, drop_first=True)

    mean_default = y.mean()

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