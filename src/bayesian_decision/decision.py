import os
from dataclasses import dataclass

import pandas as pd

from src.utils.config import ARTIFACTS_DIR


BAYESIAN_ARTIFACT_DIR = ARTIFACTS_DIR / "bayesian_decision"

INPUT_PATH = BAYESIAN_ARTIFACT_DIR / "uncertainty_summary.csv"
OUTPUT_PATH = BAYESIAN_ARTIFACT_DIR / "bayesian_decisions.csv"


@dataclass(frozen=True)
class BayesianDecisionConfig:
    prob_negative_threshold: float = 0.15
    ev_p05_threshold: float = -25.0
    ev_p05_reject_threshold: float = -100.0
    prob_negative_reject_threshold: float = 0.5


def apply_bayesian_decision(df: pd.DataFrame, config: BayesianDecisionConfig) -> pd.DataFrame:
    out = df.copy()

    decisions = []

    for _, row in out.iterrows():
        ev_mean = row["simulated_ev_mean"]
        ev_p05 = row["simulated_ev_p05"]
        prob_neg = row["prob_ev_negative"]

        if row["offer_name"] == "no_offer":
            decision = "REJECT"

        elif (
            (ev_mean > 0)
            and (prob_neg < config.prob_negative_threshold)
            and (ev_p05 > config.ev_p05_threshold)
        ):
            decision = "APPROVE"

        elif (
            (prob_neg > config.prob_negative_reject_threshold)
            or (ev_p05 < config.ev_p05_reject_threshold)
        ):
            decision = "REJECT"

        else:
            decision = "REVIEW"

        decisions.append(decision)

    out["bayesian_decision"] = decisions

    return out


def run_bayesian_decision():
    print("\n===== BAYESIAN DECISION LAYER =====")

    df = pd.read_csv(INPUT_PATH)

    config = BayesianDecisionConfig()

    df = apply_bayesian_decision(df, config)

    os.makedirs(BAYESIAN_ARTIFACT_DIR, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nDecision distribution:")
    print(df["bayesian_decision"].value_counts().to_string())

    print("\nSample decisions:")
    print(
        df[
            [
                "customer_id",
                "offer_name",
                "simulated_ev_mean",
                "simulated_ev_p05",
                "prob_ev_negative",
                "bayesian_decision",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    run_bayesian_decision()