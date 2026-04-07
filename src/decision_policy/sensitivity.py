import pandas as pd
from itertools import product

from src.utils import config
from src.decision_policy.decision_engine import apply_decision_policy
from src.decision_policy.reporting import build_portfolio_summary


BEST_OFFERS_PATH = (
    config.ARTIFACTS_DIR / "pricing_strategy" / "best_offers.csv"
)


def run_policy_sensitivity():
    print("\n===== MODULE 04: POLICY SENSITIVITY =====")

    df = pd.read_csv(BEST_OFFERS_PATH)
    print(df["p_accept"].describe())
    print(df["adjusted_p_default"].describe())

    # =========================
    # GRID (KEEP SMALL)
    # =========================
    acceptance_thresholds = [0.05, 0.10, 0.20, 0.30, 0.40]
    default_thresholds = [0.20, 0.25, 0.30, 0.40]

    results = []

    for acc_t, def_t in product(acceptance_thresholds, default_thresholds):

        # override config temporarily
        original_acc = config.MIN_ACCEPTANCE_THRESHOLD
        original_def = config.DEFAULT_APPROVAL_THRESHOLD

        config.MIN_ACCEPTANCE_THRESHOLD = acc_t
        config.DEFAULT_APPROVAL_THRESHOLD = def_t

        final_df = apply_decision_policy(df.copy())
        summary = build_portfolio_summary(final_df)

        results.append({
            "acceptance_threshold": acc_t,
            "default_threshold": def_t,
            "approval_rate": summary["approval_rate"],
            "approved_expected_value": summary["approved_expected_value"],
            "avg_p_default_approved": summary["average_adjusted_p_default_approved"],
            "avg_p_accept_approved": summary["average_p_accept_approved"],
        })

        # restore config
        config.MIN_ACCEPTANCE_THRESHOLD = original_acc
        config.DEFAULT_APPROVAL_THRESHOLD = original_def

    results_df = pd.DataFrame(results)

    print("\n===== SENSITIVITY RESULTS =====")
    print(results_df.to_string(index=False))

    out_path = (
        config.ARTIFACTS_DIR / "pricing_strategy" / "policy_sensitivity.csv"
    )
    results_df.to_csv(out_path, index=False)

    print(f"\nSaved sensitivity results to: {out_path}")