import os
import pandas as pd

from src.pricing_strategy.risk_adjustment import apply_risk_adjustment
from src.pricing_strategy.value_scoring import score_offers
from src.credit_approval.inference import add_base_risk

from src.utils.config import RESPONSE_MODELING_FEATURES_PATH
from src.utils.schema import (
    ADJUSTED_P_DEFAULT,
    CUSTOMER_ID,
    EXPECTED_VALUE,
    OFFER_NAME,
    P_ACCEPT,
)


def load_base_data() -> pd.DataFrame:
    df = pd.read_csv(RESPONSE_MODELING_FEATURES_PATH)

    if df.empty:
        raise ValueError("Response dataset is empty.")

    return df


def choose_best_offers(df: pd.DataFrame) -> pd.DataFrame:
    required = [CUSTOMER_ID, OFFER_NAME, P_ACCEPT, EXPECTED_VALUE]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for selection: {missing}")

    selected_rows = []

    for customer_id, group in df.groupby(CUSTOMER_ID, sort=False):
        valid = group[
            (
                (group[EXPECTED_VALUE] > 0) &
                (group[P_ACCEPT] >= 0.10)
            ) |
            (
                (group[OFFER_NAME] == "low_apr") &
                (group[EXPECTED_VALUE] > -25) &
                (group[P_ACCEPT] >= 0.20)
            )
        ]

        if not valid.empty:
            best = valid.loc[valid[EXPECTED_VALUE].idxmax()].copy()
            best["selection_reason"] = "selected_positive_ev"
        else:
            low_accept = group[P_ACCEPT] < 0.10
            neg_value = group[EXPECTED_VALUE] <= 0

            if neg_value.all():
                reason = "all_negative_value"
            elif low_accept.all():
                reason = "all_low_acceptance"
            else:
                reason = "mixed_constraints"

            best = group.iloc[0].copy()
            best[OFFER_NAME] = "no_offer"
            best[EXPECTED_VALUE] = 0.0
            best["selection_reason"] = reason

        selected_rows.append(best)

    result = pd.DataFrame(selected_rows).reset_index(drop=True)
    return result


def print_summary(all_df: pd.DataFrame, best_df: pd.DataFrame):
    print("\n===== MODULE 03 SUMMARY =====")

    print("\nAverage p_default by offer (AFTER adjustment):")
    print(all_df.groupby(OFFER_NAME)[ADJUSTED_P_DEFAULT].mean().to_string())

    print("\nAverage expected value by offer:")
    print(all_df.groupby(OFFER_NAME)[EXPECTED_VALUE].mean().to_string())

    print("\nPositive expected value rate by offer:")
    print((all_df[EXPECTED_VALUE] > 0).groupby(all_df[OFFER_NAME]).mean().to_string())

    print("\nAverage expected value among selected offers:")
    selected_only = best_df[best_df[OFFER_NAME] != "no_offer"]
    if selected_only.empty:
        print("No selected offers.")
    else:
        print(
            selected_only.groupby(OFFER_NAME)[EXPECTED_VALUE]
            .mean()
            .to_string()
        )

    print("\nBest offer distribution:")
    print(best_df[OFFER_NAME].value_counts().to_string())

    print("\nSelection reason distribution:")
    print(best_df["selection_reason"].value_counts().to_string())

    print("\nSample output:")
    print(
        best_df[
            [
                CUSTOMER_ID,
                OFFER_NAME,
                P_ACCEPT,
                ADJUSTED_P_DEFAULT,
                EXPECTED_VALUE,
                "selection_reason",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


def run_pricing_strategy_pipeline():
    print("\nLoading response dataset...")
    df = load_base_data()

    print("adding base risk...")
    df = add_base_risk(df)

    print("Applying risk adjustment...")
    df = apply_risk_adjustment(df)

    print("Scoring offers...")
    df = score_offers(df)

    print("Selecting best offers...")
    best_df = choose_best_offers(df)

    print_summary(df, best_df)
    

    os.makedirs("artifacts/pricing_strategy", exist_ok=True)

    df.to_csv("artifacts/pricing_strategy/all_scored_offers.csv", index=False)
    best_df.to_csv("artifacts/pricing_strategy/best_offers.csv", index=False)

    return df, best_df


if __name__ == "__main__":
    run_pricing_strategy_pipeline()