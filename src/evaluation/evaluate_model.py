import pandas as pd


def evaluate_decisions(df: pd.DataFrame) -> None:
    print("\n=== DECISION DISTRIBUTION ===")
    print(df["decision"].value_counts(normalize=True))

    print("\n=== DEFAULT RATE BY DECISION ===")
    summary = df.groupby("decision")["actual_default"].mean()
    print(summary)

    print("\n=== COUNTS BY DECISION ===")
    print(df["decision"].value_counts())