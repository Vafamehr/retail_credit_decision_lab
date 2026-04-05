# src/response_modeling/train_response_model.py

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def train_response_model(
    X,
    y,
    ids,
    test_size: float = 0.2,
    random_state: int = 42,
):
    X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
        X,
        y,
        ids,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    predicted_proba = model.predict_proba(X_test_scaled)[:, 1]

    return model, scaler, predicted_proba, y_test, id_test