
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


def train_response_model(X, y, ids, test_size=0.2, random_state=42):
    """
    Train response model.

    Inputs:
        X: feature matrix
        y: target vector
        ids: customer identifiers

    Returns:
        model
        scaler
        predicted_probabilities (on test set)
        y_test
        id_test
    """

    # Split data
    X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
        X, y, ids, test_size=test_size, random_state=random_state, stratify=y
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_scaled, y_train)

    # Predict probabilities
    predicted_probabilities = model.predict_proba(X_test_scaled)[:, 1]

    return model, scaler, predicted_probabilities, y_test, id_test