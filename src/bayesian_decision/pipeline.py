from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import pandas as pd

from src.bayesian_decision.decision import (
    BayesianDecisionConfig,
    apply_bayesian_decision,
)
from src.bayesian_decision.uncertainty import (
    UncertaintyConfig,
    run_uncertainty_analysis,
)
from src.utils.config import ARTIFACTS_DIR


BAYESIAN_ARTIFACT_DIR = ARTIFACTS_DIR / "bayesian_decision"
BEST_OFFERS_PATH = ARTIFACTS_DIR / "pricing_strategy" / "best_offers.csv"
UNCERTAINTY_SUMMARY_PATH = BAYESIAN_ARTIFACT_DIR / "uncertainty_summary.csv"
BAYESIAN_DECISIONS_PATH = BAYESIAN_ARTIFACT_DIR / "bayesian_decisions.csv"


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def run_bayesian_pipeline() -> tuple[pd.DataFrame, pd.DataFrame]:
    print("\n===== BAYESIAN DECISION PIPELINE =====")

    print(f"Loading pricing output from: {BEST_OFFERS_PATH}")
    df = pd.read_csv(BEST_OFFERS_PATH)

    uncertainty_config = UncertaintyConfig(
        n_simulations=5000,
        probability_concentration=60.0,
        tail_alpha=0.05,
        random_seed=42,
    )

    decision_config = BayesianDecisionConfig(
        prob_negative_threshold=0.15,
        ev_p05_threshold=-25.0,
        ev_p05_reject_threshold=-100.0,
        prob_negative_reject_threshold=0.5,
    )

    ensure_output_dir(BAYESIAN_ARTIFACT_DIR)

    print("\nRunning uncertainty simulation...")
    summary_df = run_uncertainty_analysis(df, config=uncertainty_config)

    print(f"Saving uncertainty summary to: {UNCERTAINTY_SUMMARY_PATH}")
    summary_df.to_csv(UNCERTAINTY_SUMMARY_PATH, index=False)

    print("\nApplying Bayesian decision rules...")
    decision_df = apply_bayesian_decision(summary_df, config=decision_config)

    print(f"Saving Bayesian decisions to: {BAYESIAN_DECISIONS_PATH}")
    decision_df.to_csv(BAYESIAN_DECISIONS_PATH, index=False)

    print("\nUncertainty config:")
    print(asdict(uncertainty_config))

    print("\nDecision config:")
    print(asdict(decision_config))

    print("\nDecision distribution:")
    print(decision_df["bayesian_decision"].value_counts().to_string())

    print("\nTop rows:")
    preview_cols = [
        "customer_id",
        "offer_name",
        "adjusted_p_default",
        "p_accept",
        "expected_value",
        "simulated_ev_mean",
        "simulated_ev_p05",
        "prob_ev_negative",
        "simulated_pd_p95",
        "ev_expected_shortfall_5pct",
        "bayesian_decision",
    ]
    preview_cols = [c for c in preview_cols if c in decision_df.columns]
    print(decision_df[preview_cols].head(10).to_string(index=False))

    return summary_df, decision_df


if __name__ == "__main__":
    run_bayesian_pipeline()