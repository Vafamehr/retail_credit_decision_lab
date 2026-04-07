import pandas as pd

from src.utils import config
import src.utils.schema as schema


def apply_decision_policy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply final decision policy on best offers output.

    Input:
        df = best_offers DataFrame (one row per customer)

    Output:
        df with:
            - final_decision
            - decision_reason
            - policy_segment
    """

    df = df.copy()

    # =========================
    # POLICY SEGMENT
    # =========================

    def assign_segment(p_default: float) -> str:
        if p_default < 0.10:
            return "low_risk"
        elif p_default < 0.20:
            return "medium_risk"
        elif p_default < config.DEFAULT_APPROVAL_THRESHOLD:
            return "high_risk"
        else:
            return "outside_risk_appetite"

    df["policy_segment"] = df[schema.ADJUSTED_P_DEFAULT].apply(assign_segment)

    # =========================
    # DECISION LOGIC
    # =========================

    def decide(row):
        p_default = row[schema.ADJUSTED_P_DEFAULT]
        p_accept = row[schema.P_ACCEPT]
        ev = row[schema.EXPECTED_VALUE]
        review_flag = row[schema.REVIEW_FLAG]

        if p_default >= config.DEFAULT_APPROVAL_THRESHOLD:
            return "decline", "risk_too_high"

        if ev <= 0:
            return "decline", "negative_expected_value"

        if p_accept < config.MIN_ACCEPTANCE_THRESHOLD:
            return "decline", "low_acceptance_probability"

        if review_flag == 1:
            return "manual_review", "review_flag_triggered"

        offer_name = row[schema.OFFER_NAME]

        if offer_name == "low_apr":
            return "approve_low_apr", "approved_profitable_low_risk"
        elif offer_name == "mid_apr":
            return "approve_mid_apr", "approved_profitable_balanced"
        elif offer_name == "high_apr":
            return "approve_high_apr", "approved_high_margin"
        else:
            return "approve", "approved_default"

    decisions = df.apply(decide, axis=1)

    df["final_decision"] = decisions.apply(lambda x: x[0])
    df["decision_reason"] = decisions.apply(lambda x: x[1])

    return df