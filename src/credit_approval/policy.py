import pandas as pd


def apply_approval_policy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    conditions = [
        df["predicted_risk"] < 0.18,
        (df["predicted_risk"] >= 0.18) & (df["predicted_risk"] < 0.32),
        df["predicted_risk"] >= 0.32,
    ]

    decisions = [
        "approve",
        "review",
        "reject",
    ]

    df["decision"] = pd.Series(index=df.index, dtype="object")
    df.loc[conditions[0], "decision"] = decisions[0]
    df.loc[conditions[1], "decision"] = decisions[1]
    df.loc[conditions[2], "decision"] = decisions[2]

    return df


def main() -> None:
    sample_df = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4],
            "predicted_risk": [0.12, 0.38, 0.61, 0.82],
        }
    )

    result = apply_approval_policy(sample_df)
    print(result)


if __name__ == "__main__":
    main()