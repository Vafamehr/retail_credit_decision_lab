import pandas as pd

from src.utils.config import ARTIFACTS_DIR, DECISION_POLICY_ARTIFACT_DIR
from src.decision_policy.decision_engine import apply_decision_policy
from src.decision_policy.reporting import (
    build_portfolio_summary,
)

# Ensure output directory exists
DECISION_POLICY_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

# Input (from pricing)
BEST_OFFERS_PATH = ARTIFACTS_DIR / "pricing_strategy" / "best_offers.csv"

# Outputs (to decision_policy)
STRATEGY_COMPARISON_PATH = DECISION_POLICY_ARTIFACT_DIR / "strategy_comparison.csv"
FINAL_DECISIONS_PATH = DECISION_POLICY_ARTIFACT_DIR / "final_decisions.csv"


def run_decision_policy_pipeline():
    print("\n===== DECISION POLICY (MULTI-STRATEGY) =====")

    print("Loading best offers...")
    df = pd.read_csv(BEST_OFFERS_PATH)
    print(f"Input shape: {df.shape}")

    strategies = {
        "conservative": {
            "max_p_default": 0.25,
            "min_p_accept": 0.25,
            "min_expected_value": 20,
        },
        "balanced": {
            "max_p_default": 0.30,
            "min_p_accept": 0.20,
            "min_expected_value": 0,
        },
        "aggressive": {
            "max_p_default": 0.40,
            "min_p_accept": 0.10,
            "min_expected_value": -10,
        },
        "aggressive_with_risk_cap": {
            "max_p_default": 0.40,
            "min_p_accept": 0.10,
            "min_expected_value": -10,
            "risk_cap": 0.22,
        },
    }

    results = []
    last_strat_df = None

    for name, params in strategies.items():
        print(f"\n--- Running strategy: {name} ---")

        strat_df = apply_decision_policy(
            df,
            max_p_default=params["max_p_default"],
            min_p_accept=params["min_p_accept"],
            min_expected_value=params["min_expected_value"],
        )

        risk_cap = params.get("risk_cap")

        if risk_cap is not None:
            strat_df = strat_df.copy()

            mask = (
                strat_df["final_decision"].str.startswith("approve") &
                (strat_df["adjusted_p_default"] > risk_cap)
            )

            strat_df.loc[mask, "final_decision"] = "decline"
            strat_df.loc[mask, "decision_reason"] = "risk_cap_exceeded"

        summary = build_portfolio_summary(strat_df)

        summary["strategy"] = name
        summary["max_p_default"] = params["max_p_default"]
        summary["min_p_accept"] = params["min_p_accept"]
        summary["min_expected_value"] = params["min_expected_value"]
        summary["risk_cap"] = risk_cap if risk_cap is not None else None

        results.append(summary)

        # keep last (or you can switch to best later)
        last_strat_df = strat_df

    comparison_df = pd.DataFrame(results)

    print("\n===== STRATEGY COMPARISON =====")
    print(comparison_df.to_string(index=False))

    # Save outputs
    comparison_df.to_csv(STRATEGY_COMPARISON_PATH, index=False)

    if last_strat_df is not None:
        last_strat_df.to_csv(FINAL_DECISIONS_PATH, index=False)

    print(f"\nSaved strategy comparison to: {STRATEGY_COMPARISON_PATH}")
    print(f"Saved final decisions to: {FINAL_DECISIONS_PATH}")
    print("===== DONE =====\n")