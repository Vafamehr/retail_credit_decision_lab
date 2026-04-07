import pandas as pd

from src.utils.config import ARTIFACTS_DIR
from src.decision_policy.decision_engine import apply_decision_policy
from src.decision_policy.reporting import (
    build_portfolio_summary,
    build_decision_breakdown,
    build_decision_reason_breakdown,
    build_segment_breakdown,
    build_segment_decision_breakdown,
    build_reason_by_segment_breakdown,
    print_portfolio_summary,
)


PRICING_ARTIFACT_DIR = ARTIFACTS_DIR / "pricing_strategy"

BEST_OFFERS_PATH = PRICING_ARTIFACT_DIR / "best_offers.csv"
FINAL_DECISIONS_PATH = PRICING_ARTIFACT_DIR / "final_decisions.csv"
DECISION_BREAKDOWN_PATH = PRICING_ARTIFACT_DIR / "decision_breakdown.csv"
DECISION_REASON_BREAKDOWN_PATH = PRICING_ARTIFACT_DIR / "decision_reason_breakdown.csv"
SEGMENT_BREAKDOWN_PATH = PRICING_ARTIFACT_DIR / "segment_breakdown.csv"
SEGMENT_DECISION_BREAKDOWN_PATH = (
    PRICING_ARTIFACT_DIR / "segment_decision_breakdown.csv"
)
REASON_BY_SEGMENT_BREAKDOWN_PATH = (
    PRICING_ARTIFACT_DIR / "reason_by_segment_breakdown.csv"
)


def run_decision_policy_pipeline():
    print("\n===== MODULE 04: DECISION POLICY =====")

    # =========================
    # LOAD INPUT
    # =========================
    print("Loading best offers...")
    df = pd.read_csv(BEST_OFFERS_PATH)
    print(f"Input shape: {df.shape}")

    # =========================
    # APPLY POLICY
    # =========================
    print("Applying decision policy...")
    final_df = apply_decision_policy(df)

    # =========================
    # BUILD REPORTS
    # =========================
    print("Building portfolio reports...")
    portfolio_summary = build_portfolio_summary(final_df)
    decision_breakdown = build_decision_breakdown(final_df)
    decision_reason_breakdown = build_decision_reason_breakdown(final_df)
    segment_breakdown = build_segment_breakdown(final_df)
    segment_decision_breakdown = build_segment_decision_breakdown(final_df)
    reason_by_segment_breakdown = build_reason_by_segment_breakdown(final_df)

    # =========================
    # PRINT SUMMARY
    # =========================
    print_portfolio_summary(portfolio_summary)

    print("\n===== DECISION BREAKDOWN =====")
    print(decision_breakdown.to_string(index=False))

    print("\n===== DECISION REASON BREAKDOWN =====")
    print(decision_reason_breakdown.to_string(index=False))

    print("\n===== SEGMENT BREAKDOWN =====")
    print(segment_breakdown.to_string(index=False))

    print("\n===== SEGMENT x DECISION BREAKDOWN =====")
    print(segment_decision_breakdown.to_string(index=False))

    print("\n===== SEGMENT x REASON BREAKDOWN =====")
    print(reason_by_segment_breakdown.to_string(index=False))

    # =========================
    # SAVE OUTPUTS
    # =========================
    final_df.to_csv(FINAL_DECISIONS_PATH, index=False)
    decision_breakdown.to_csv(DECISION_BREAKDOWN_PATH, index=False)
    decision_reason_breakdown.to_csv(DECISION_REASON_BREAKDOWN_PATH, index=False)
    segment_breakdown.to_csv(SEGMENT_BREAKDOWN_PATH, index=False)
    segment_decision_breakdown.to_csv(
        SEGMENT_DECISION_BREAKDOWN_PATH, index=False
    )
    reason_by_segment_breakdown.to_csv(
        REASON_BY_SEGMENT_BREAKDOWN_PATH, index=False
    )

    print(f"\nSaved final decisions to: {FINAL_DECISIONS_PATH}")
    print(f"Saved decision breakdown to: {DECISION_BREAKDOWN_PATH}")
    print(f"Saved decision reason breakdown to: {DECISION_REASON_BREAKDOWN_PATH}")
    print(f"Saved segment breakdown to: {SEGMENT_BREAKDOWN_PATH}")
    print(
        f"Saved segment x decision breakdown to: "
        f"{SEGMENT_DECISION_BREAKDOWN_PATH}"
    )
    print(
        f"Saved segment x reason breakdown to: "
        f"{REASON_BY_SEGMENT_BREAKDOWN_PATH}"
    )
    print("===== DONE =====\n")