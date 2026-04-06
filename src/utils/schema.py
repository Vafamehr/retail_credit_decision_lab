"""
Canonical schema for the Retail Credit Decision Lab.

This file defines:
- raw/base column names
- engineered feature names
- offer-level feature names
- target names
- required column groups by module

One meaning = one canonical name.
"""

# =========================
# IDENTIFIERS
# =========================

CUSTOMER_ID = "customer_id"


# =========================
# BASE CUSTOMER / LOAN COLUMNS
# =========================

ANNUAL_INCOME = "annual_income"
LOAN_AMOUNT = "loan_amount"
LOAN_TERM = "loan_term"
CREDIT_SCORE = "credit_score"
AGE = "age"
EMPLOYMENT_LENGTH_YEARS = "employment_length_years"
DEBT_TO_INCOME = "debt_to_income"
CREDIT_UTILIZATION = "credit_utilization"
DELINQUENCY_COUNT = "delinquency_count"
INQUIRY_COUNT = "inquiry_count"

EXISTING_CUSTOMER = "existing_customer"
RELATIONSHIP_TENURE_MONTHS = "relationship_tenure_months"
NUM_EXISTING_PRODUCTS = "num_existing_products"


# =========================
# ENGINEERED RISK FEATURES
# =========================

LOAN_TO_INCOME_RATIO = "loan_to_income_ratio"
INCOME_PER_MONTH = "income_per_month"
ESTIMATED_MONTHLY_PAYMENT = "estimated_monthly_payment"
PAYMENT_TO_INCOME_RATIO = "payment_to_income_ratio"
RISK_SCORE_BAND = "risk_score_band"
REVIEW_FLAG = "review_flag"


# =========================
# OFFER / PRICING COLUMNS
# =========================

OFFER_NAME = "offer_name"
OFFERED_INTEREST_RATE = "offered_interest_rate"


# =========================
# TARGET / PREDICTION COLUMNS
# =========================

DEFAULT_TARGET = "default"
ACCEPTED_OFFER = "accepted_offer"

P_DEFAULT = "p_default"
BASE_P_DEFAULT = "base_p_default"
ADJUSTED_P_DEFAULT = "adjusted_p_default"
P_ACCEPT = "p_accept"
RESPONSE_PROBABILITY = "response_probability"

EXPECTED_REVENUE = "expected_revenue"
EXPECTED_LOSS = "expected_loss"
EXPECTED_VALUE = "expected_value"


# =========================
# MODULE 03 SUPPORT COLUMNS
# =========================

APPROVAL_DECISION = "approval_decision"
REVIEW_DECISION = "review_decision"
REJECT_DECISION = "reject_decision"

RISK_UPLIFT = "risk_uplift"
RISK_ADJUSTMENT_FACTOR = "risk_adjustment_factor"


# =========================
# COLUMN GROUPS
# =========================

IDENTIFIER_COLUMNS = [
    CUSTOMER_ID,
]

BASE_INPUT_COLUMNS = [
    CUSTOMER_ID,
    ANNUAL_INCOME,
    LOAN_AMOUNT,
    LOAN_TERM,
    CREDIT_SCORE,
    AGE,
    EMPLOYMENT_LENGTH_YEARS,
    DEBT_TO_INCOME,
    CREDIT_UTILIZATION,
    DELINQUENCY_COUNT,
    INQUIRY_COUNT,
    EXISTING_CUSTOMER,
    RELATIONSHIP_TENURE_MONTHS,
    NUM_EXISTING_PRODUCTS,
]

ENGINEERED_FEATURE_COLUMNS = [
    LOAN_TO_INCOME_RATIO,
    INCOME_PER_MONTH,
    ESTIMATED_MONTHLY_PAYMENT,
    PAYMENT_TO_INCOME_RATIO,
    RISK_SCORE_BAND,
    REVIEW_FLAG,
]

CREDIT_APPROVAL_FEATURE_COLUMNS = [
    ANNUAL_INCOME,
    LOAN_AMOUNT,
    LOAN_TERM,
    CREDIT_SCORE,
    AGE,
    EMPLOYMENT_LENGTH_YEARS,
    DEBT_TO_INCOME,
    CREDIT_UTILIZATION,
    DELINQUENCY_COUNT,
    INQUIRY_COUNT,
    EXISTING_CUSTOMER,
    RELATIONSHIP_TENURE_MONTHS,
    NUM_EXISTING_PRODUCTS,
    LOAN_TO_INCOME_RATIO,
    INCOME_PER_MONTH,
    ESTIMATED_MONTHLY_PAYMENT,
    PAYMENT_TO_INCOME_RATIO,
]

OFFER_FEATURE_COLUMNS = [
    OFFER_NAME,
    OFFERED_INTEREST_RATE,
    ESTIMATED_MONTHLY_PAYMENT,
    PAYMENT_TO_INCOME_RATIO,
]

RESPONSE_MODELING_FEATURE_COLUMNS = [
    ANNUAL_INCOME,
    LOAN_AMOUNT,
    LOAN_TERM,
    CREDIT_SCORE,
    AGE,
    EMPLOYMENT_LENGTH_YEARS,
    DEBT_TO_INCOME,
    CREDIT_UTILIZATION,
    DELINQUENCY_COUNT,
    INQUIRY_COUNT,
    EXISTING_CUSTOMER,
    RELATIONSHIP_TENURE_MONTHS,
    NUM_EXISTING_PRODUCTS,
    LOAN_TO_INCOME_RATIO,
    INCOME_PER_MONTH,
    ESTIMATED_MONTHLY_PAYMENT,
    PAYMENT_TO_INCOME_RATIO,
    OFFERED_INTEREST_RATE,
]

MODULE_03_REQUIRED_COLUMNS = [
    CUSTOMER_ID,
    OFFER_NAME,
    OFFERED_INTEREST_RATE,
    ESTIMATED_MONTHLY_PAYMENT,
    PAYMENT_TO_INCOME_RATIO,
    BASE_P_DEFAULT,
    P_ACCEPT,
]

DEFAULT_TARGET_COLUMNS = [
    DEFAULT_TARGET,
]

RESPONSE_TARGET_COLUMNS = [
    ACCEPTED_OFFER,
]


# =========================
# OPTIONAL GROUPINGS
# =========================

NUMERIC_BASE_COLUMNS = [
    ANNUAL_INCOME,
    LOAN_AMOUNT,
    LOAN_TERM,
    CREDIT_SCORE,
    AGE,
    EMPLOYMENT_LENGTH_YEARS,
    DEBT_TO_INCOME,
    CREDIT_UTILIZATION,
    DELINQUENCY_COUNT,
    INQUIRY_COUNT,
    RELATIONSHIP_TENURE_MONTHS,
    NUM_EXISTING_PRODUCTS,
]

NUMERIC_ENGINEERED_COLUMNS = [
    LOAN_TO_INCOME_RATIO,
    INCOME_PER_MONTH,
    ESTIMATED_MONTHLY_PAYMENT,
    PAYMENT_TO_INCOME_RATIO,
    OFFERED_INTEREST_RATE,
]

BINARY_COLUMNS = [
    EXISTING_CUSTOMER,
    REVIEW_FLAG,
]

PREDICTION_OUTPUT_COLUMNS = [
    BASE_P_DEFAULT,
    ADJUSTED_P_DEFAULT,
    P_DEFAULT,
    P_ACCEPT,
    EXPECTED_REVENUE,
    EXPECTED_LOSS,
    EXPECTED_VALUE,
]


# =========================
# SIMPLE VALIDATION HELPERS
# =========================

def missing_columns(df, required_columns):
    """
    Return a list of missing columns from a dataframe.
    """
    return [col for col in required_columns if col not in df.columns]