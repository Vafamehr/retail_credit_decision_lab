"""
Central configuration for the Retail Credit Decision Lab.

This file is the single source of truth for:
- shared data paths
- artifact locations
- pricing assumptions
- global thresholds

Keep this lightweight and explicit.
"""

from pathlib import Path


# =========================
# BASE PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"


# =========================
# DATA PATHS
# =========================

# Shared data
SHARED_DATA_DIR = DATA_DIR / "shared"
SHARED_PROCESSED_DIR = SHARED_DATA_DIR / "processed"

SYNTHETIC_LOAN_DATA_PATH = SHARED_DATA_DIR / "synthetic_loan_data.csv"
LOAN_FEATURES_PATH = SHARED_PROCESSED_DIR / "loan_features.csv"

# Response modeling data
RESPONSE_MODELING_DATA_DIR = DATA_DIR / "response_modeling"
RESPONSE_MODELING_PROCESSED_DIR = RESPONSE_MODELING_DATA_DIR / "processed"

RESPONSE_MODELING_FEATURES_PATH = (
    RESPONSE_MODELING_PROCESSED_DIR / "response_modeling_features.csv"
)


# =========================
# MODEL NAMES
# =========================

CREDIT_APPROVAL_MODEL_NAME = "logistic_regression"
RESPONSE_MODELING_MODEL_NAME = "logistic_regression"


# =========================
# ARTIFACT PATHS
# =========================

# Credit approval
CREDIT_APPROVAL_ARTIFACT_DIR = ARTIFACTS_DIR / "credit_approval"
CREDIT_APPROVAL_MODEL_DIR = (
    CREDIT_APPROVAL_ARTIFACT_DIR / CREDIT_APPROVAL_MODEL_NAME
)

CREDIT_MODEL_PATH = CREDIT_APPROVAL_MODEL_DIR / "model.pkl"
CREDIT_SCALER_PATH = CREDIT_APPROVAL_MODEL_DIR / "scaler.pkl"
CREDIT_FEATURE_COLUMNS_PATH = CREDIT_APPROVAL_MODEL_DIR / "feature_columns.pkl"

# Response modeling
RESPONSE_MODELING_ARTIFACT_DIR = ARTIFACTS_DIR / "response_modeling"
RESPONSE_MODELING_MODEL_DIR = (
    RESPONSE_MODELING_ARTIFACT_DIR / RESPONSE_MODELING_MODEL_NAME
)

RESPONSE_MODEL_PATH = RESPONSE_MODELING_MODEL_DIR / "model.pkl"
RESPONSE_SCALER_PATH = RESPONSE_MODELING_MODEL_DIR / "scaler.pkl"
RESPONSE_FEATURE_COLUMNS_PATH = RESPONSE_MODELING_MODEL_DIR / "feature_columns.pkl"


# =========================
# PRICING / RISK SETTINGS
# =========================

APR_OPTIONS = {
    "low_apr": 0.12,
    "mid_apr": 0.18,
    "high_apr": 0.24,
}

LOSS_GIVEN_DEFAULT = 0.45


# =========================
# DECISION THRESHOLDS
# =========================

MIN_ACCEPTANCE_THRESHOLD = 0.20
DEFAULT_APPROVAL_THRESHOLD = 0.30


# =========================
# MODULE 03 RISK UPLIFT
# =========================

# Compact, interview-defensible offer-adjusted risk layer.
# Higher APR / payment burden should increase risk relative to base borrower risk.
RISK_UPLIFT_COEFFICIENTS = {
    "interest_rate": 0.35,
    "payment_to_income_ratio": 0.45,
    "monthly_payment_log": 0.05,
}

# Used as neutral anchors for uplift calculations.
BASELINE_INTEREST_RATE = APR_OPTIONS["mid_apr"]
BASELINE_PAYMENT_TO_INCOME_RATIO = 0.12


# =========================
# HELPERS
# =========================

def ensure_directories() -> None:
    """
    Create required directories if they do not exist.
    Safe to call from any pipeline.
    """
    required_dirs = [
        SHARED_DATA_DIR,
        SHARED_PROCESSED_DIR,
        RESPONSE_MODELING_DATA_DIR,
        RESPONSE_MODELING_PROCESSED_DIR,
        CREDIT_APPROVAL_ARTIFACT_DIR,
        CREDIT_APPROVAL_MODEL_DIR,
        RESPONSE_MODELING_ARTIFACT_DIR,
        RESPONSE_MODELING_MODEL_DIR,
    ]

    for directory in required_dirs:
        directory.mkdir(parents=True, exist_ok=True)