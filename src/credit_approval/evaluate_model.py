import pandas as pd

from src.utils.schema import DEFAULT_TARGET


def evaluate_decisions(df: pd.DataFrame) -> None:
    if DEFAULT_TARGET not in df.columns:
        raise ValueError(
            f"Required column '{DEFAULT_TARGET}' not found in input DataFrame."
        )

    print("\n=== DECISION DISTRIBUTION ===")
    print(df["decision"].value_counts(normalize=True))

    print("\n=== DEFAULT RATE BY DECISION ===")
    summary = df.groupby("decision")[DEFAULT_TARGET].mean()
    print(summary)

    print("\n=== COUNTS BY DECISION ===")
    print(df["decision"].value_counts())