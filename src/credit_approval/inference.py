import pandas as pd
import joblib

from src.utils.config import (
    CREDIT_FEATURE_COLUMNS_PATH,
    CREDIT_MODEL_PATH,
    CREDIT_SCALER_PATH,
)
from src.utils.schema import (
    BASE_P_DEFAULT,
    CREDIT_APPROVAL_FEATURE_COLUMNS,
    missing_columns,
)


def load_artifacts():
    model = joblib.load(CREDIT_MODEL_PATH)
    scaler = joblib.load(CREDIT_SCALER_PATH)
    feature_columns = joblib.load(CREDIT_FEATURE_COLUMNS_PATH)

    return model, scaler, feature_columns


def prepare_features(df: pd.DataFrame, feature_columns: list) -> pd.DataFrame:
    """
    Align input dataframe to training feature space.
    """
    X = df.copy()

    X = pd.get_dummies(X, drop_first=True)

    for col in feature_columns:
        if col not in X.columns:
            X[col] = 0

    X = X[feature_columns]

    return X


def predict_base_risk(df: pd.DataFrame) -> pd.Series:
    """
    Predict base borrower default probability.
    """
    required = CREDIT_APPROVAL_FEATURE_COLUMNS
    missing = missing_columns(df, required)

    if missing:
        raise ValueError(f"Missing required columns for credit inference: {missing}")

    model, scaler, feature_columns = load_artifacts()

    X = prepare_features(df[required], feature_columns)
    X_scaled = scaler.transform(X)

    p_default = model.predict_proba(X_scaled)[:, 1]

    return pd.Series(p_default, index=df.index, name=BASE_P_DEFAULT)


def add_base_risk(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add base_p_default to dataframe.
    """
    out = df.copy()
    out[BASE_P_DEFAULT] = predict_base_risk(out)
    return out