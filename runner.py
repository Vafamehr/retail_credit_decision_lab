from src.data.generate_data import main as generate_data
from src.features.feature_engineering import main as build_features
from src.credit_approval.pipeline import run_credit_approval_pipeline
from src.response_modeling.pipeline import run_response_modeling_pipeline
from src.pricing_strategy.pipeline import run_pricing_strategy_pipeline
from src.decision_policy.pipeline import run_decision_policy_pipeline


def run_full_pipeline():
    print("\n==============================")
    print("STEP 1: Generate Synthetic Data")
    print("==============================")
    generate_data()

    print("\n==============================")
    print("STEP 2: Feature Engineering")
    print("==============================")
    build_features()

    print("\n==============================")
    print("STEP 3: Credit Approval Model")
    print("==============================")
    run_credit_approval_pipeline()

    print("\n==============================")
    print("STEP 4: Response Model")
    print("==============================")
    run_response_modeling_pipeline()

    print("\n==============================")
    print("STEP 5: Pricing Strategy")
    print("==============================")
    run_pricing_strategy_pipeline()

    print("\n==============================")
    print("STEP 6: Decision Policy")
    print("==============================")
    run_decision_policy_pipeline()

    print("\n==============================")
    print("PIPELINE COMPLETE")
    print("==============================")


if __name__ == "__main__":
    run_full_pipeline()