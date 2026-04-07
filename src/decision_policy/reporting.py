import pandas as pd

import src.utils.schema as schema


FINAL_DECISION_COL = "final_decision"
DECISION_REASON_COL = "decision_reason"
POLICY_SEGMENT_COL = "policy_segment"


def _safe_mean(series: pd.Series) -> float:
    if len(series) == 0:
        return 0.0
    return float(series.mean())


def build_portfolio_summary(df: pd.DataFrame) -> dict:
    """
    Build portfolio-level summary metrics from final decision outputs.
    """

    total_customers = len(df)

    approved_mask = df[FINAL_DECISION_COL].isin(
        ["approve_low_apr", "approve_mid_apr", "approve_high_apr", "approve"]
    )
    declined_mask = df[FINAL_DECISION_COL] == "decline"
    review_mask = df[FINAL_DECISION_COL] == "manual_review"

    approved_df = df[approved_mask]
    declined_df = df[declined_mask]
    review_df = df[review_mask]

    summary = {
        "total_customers": int(total_customers),
        "approved_customers": int(len(approved_df)),
        "declined_customers": int(len(declined_df)),
        "manual_review_customers": int(len(review_df)),
        "approval_rate": round(len(approved_df) / total_customers, 4) if total_customers else 0.0,
        "decline_rate": round(len(declined_df) / total_customers, 4) if total_customers else 0.0,
        "manual_review_rate": round(len(review_df) / total_customers, 4) if total_customers else 0.0,
        "total_expected_value": round(float(df[schema.EXPECTED_VALUE].sum()), 2),
        "approved_expected_value": round(float(approved_df[schema.EXPECTED_VALUE].sum()), 2),
        "average_expected_value_all": round(_safe_mean(df[schema.EXPECTED_VALUE]), 4),
        "average_expected_value_approved": round(_safe_mean(approved_df[schema.EXPECTED_VALUE]), 4),
        "average_adjusted_p_default_approved": round(
            _safe_mean(approved_df[schema.ADJUSTED_P_DEFAULT]), 4
        ),
        "average_p_accept_approved": round(
            _safe_mean(approved_df[schema.P_ACCEPT]), 4
        ),
    }

    return summary


def build_decision_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count and rate by final decision.
    """
    counts = (
        df[FINAL_DECISION_COL]
        .value_counts(dropna=False)
        .rename_axis(FINAL_DECISION_COL)
        .reset_index(name="count")
    )
    counts["rate"] = counts["count"] / len(df) if len(df) else 0.0
    return counts


def build_decision_reason_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count and rate by decision reason.
    """
    counts = (
        df[DECISION_REASON_COL]
        .value_counts(dropna=False)
        .rename_axis(DECISION_REASON_COL)
        .reset_index(name="count")
    )
    counts["rate"] = counts["count"] / len(df) if len(df) else 0.0
    return counts


def build_segment_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count and rate by policy segment.
    """
    counts = (
        df[POLICY_SEGMENT_COL]
        .value_counts(dropna=False)
        .rename_axis(POLICY_SEGMENT_COL)
        .reset_index(name="count")
    )
    counts["rate"] = counts["count"] / len(df) if len(df) else 0.0
    return counts


def build_segment_decision_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cross-tab of policy segment x final decision.
    """
    out = (
        df.groupby([POLICY_SEGMENT_COL, FINAL_DECISION_COL])
        .size()
        .reset_index(name="count")
        .sort_values([POLICY_SEGMENT_COL, "count"], ascending=[True, False])
    )
    return out


def build_reason_by_segment_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cross-tab of policy segment x decision reason.
    """
    out = (
        df.groupby([POLICY_SEGMENT_COL, DECISION_REASON_COL])
        .size()
        .reset_index(name="count")
        .sort_values([POLICY_SEGMENT_COL, "count"], ascending=[True, False])
    )
    return out


def print_portfolio_summary(summary: dict) -> None:
    print("\n===== PORTFOLIO SUMMARY =====")
    for key, value in summary.items():
        print(f"{key}: {value}")