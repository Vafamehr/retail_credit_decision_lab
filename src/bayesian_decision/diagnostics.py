from pathlib import Path

import pandas as pd

from src.utils.config import ARTIFACTS_DIR

PRICING_ARTIFACT_DIR = ARTIFACTS_DIR / "pricing_strategy"
BEST_OFFERS_PATH = PRICING_ARTIFACT_DIR / "best_offers.csv"


NUMERIC_COLUMNS = [
    "expected_value",
    "expected_revenue",
    "expected_loss",
    "p_accept",
    "adjusted_p_default",
]


def print_separator(title: str):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def run_diagnostics():
    print_separator("LOADING DATA")

    df = pd.read_csv(BEST_OFFERS_PATH)
    print(f"Loaded {len(df)} rows")

    print_separator("BASIC INFO")
    print(df[NUMERIC_COLUMNS].describe())

    print_separator("MEAN VALUES")
    print(df[NUMERIC_COLUMNS].mean())

    print_separator("MEDIAN VALUES")
    print(df[NUMERIC_COLUMNS].median())

    print_separator("NEGATIVE EV RATE")
    neg_rate = (df["expected_value"] < 0).mean()
    print(f"Fraction of negative EV rows: {neg_rate:.4f}")

    print_separator("ZERO / LOW ACCEPTANCE CHECK")
    print(df["p_accept"].describe())

    print_separator("DEFAULT PROBABILITY CHECK")
    print(df["adjusted_p_default"].describe())

    print_separator("REVENUE VS LOSS COMPARISON")

    df["rev_minus_loss"] = df["expected_revenue"] - df["expected_loss"]

    print(df["rev_minus_loss"].describe())

    print("\nSample rows (revenue vs loss):")
    print(
        df[
            [
                "expected_revenue",
                "expected_loss",
                "rev_minus_loss",
                "expected_value",
            ]
        ]
        .head(10)
    )

    print_separator("TOP 10 WORST EV ROWS")
    print(
        df.sort_values("expected_value")
        .head(10)[
            [
                "expected_value",
                "expected_revenue",
                "expected_loss",
                "p_accept",
                "adjusted_p_default",
            ]
        ]
    )

    print_separator("TOP 10 BEST EV ROWS")
    print(
        df.sort_values("expected_value", ascending=False)
        .head(10)[
            [
                "expected_value",
                "expected_revenue",
                "expected_loss",
                "p_accept",
                "adjusted_p_default",
            ]
        ]
    )


if __name__ == "__main__":
    run_diagnostics()