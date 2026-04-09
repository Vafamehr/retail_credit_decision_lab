from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "customer_id",
    "offer_name",
    "adjusted_p_default",
    "p_accept",
    "expected_revenue",
    "expected_loss",
    "expected_value",
]


@dataclass(frozen=True)
class UncertaintyConfig:
    n_simulations: int = 5000
    probability_concentration: float = 60.0
    tail_alpha: float = 0.05
    random_seed: int = 42


def validate_input_columns(df: pd.DataFrame, required_columns: Iterable[str] = REQUIRED_COLUMNS) -> None:
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(
            "Missing required columns for Bayesian uncertainty module: "
            f"{missing}. Available columns: {df.columns.tolist()}"
        )


def clip_probabilities(series: pd.Series, eps: float = 1e-6) -> pd.Series:
    return series.clip(lower=eps, upper=1.0 - eps)


def beta_parameterize_from_mean(mean: pd.Series, concentration: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Convert a probability mean into Beta(alpha, beta) parameters using:
        alpha = mean * concentration
        beta  = (1 - mean) * concentration

    Interpretation:
    - mean controls center
    - concentration controls certainty / spread
    """
    clipped_mean = clip_probabilities(mean)
    alpha = (clipped_mean * concentration).to_numpy(dtype=float)
    beta = ((1.0 - clipped_mean) * concentration).to_numpy(dtype=float)
    return alpha, beta


def simulate_beta_draws(alpha: np.ndarray, beta: np.ndarray, n_simulations: int, rng: np.random.Generator) -> np.ndarray:
    """
    Returns array of shape (n_rows, n_simulations)
    """
    return rng.beta(alpha[:, None], beta[:, None], size=(len(alpha), n_simulations))


def compute_simulated_ev(
    p_default_draws: np.ndarray,
    p_accept_draws: np.ndarray,
    expected_revenue: np.ndarray,
    expected_loss: np.ndarray,
) -> np.ndarray:
    """
    Economic propagation:
        EV = p_accept * [ (1 - p_default) * expected_revenue - p_default * expected_loss ]

    expected_revenue: payoff in good outcome
    expected_loss: magnitude of bad outcome loss
    """
    return p_accept_draws * (
        (1.0 - p_default_draws) * expected_revenue[:, None]
        - p_default_draws * expected_loss[:, None]
    )


def expected_shortfall(values: np.ndarray, alpha: float) -> np.ndarray:
    """
    Row-wise expected shortfall (CVaR-style tail mean) for the worst alpha fraction.
    Lower values are worse because this is EV.
    """
    threshold = np.quantile(values, alpha, axis=1)
    out = np.empty(values.shape[0], dtype=float)

    for i in range(values.shape[0]):
        tail = values[i, values[i] <= threshold[i]]
        if tail.size == 0:
            out[i] = threshold[i]
        else:
            out[i] = tail.mean()

    return out


def summarize_uncertainty(
    df: pd.DataFrame,
    simulated_pd: np.ndarray,
    simulated_accept: np.ndarray,
    simulated_ev: np.ndarray,
    tail_alpha: float,
) -> pd.DataFrame:
    ev_p05 = np.quantile(simulated_ev, tail_alpha, axis=1)
    ev_p50 = np.quantile(simulated_ev, 0.50, axis=1)
    ev_p95 = np.quantile(simulated_ev, 0.95, axis=1)

    pd_p95 = np.quantile(simulated_pd, 0.95, axis=1)

    summary = df.copy()

    summary["simulated_pd_mean"] = simulated_pd.mean(axis=1)
    summary["simulated_pd_p95"] = pd_p95

    summary["simulated_accept_mean"] = simulated_accept.mean(axis=1)

    summary["simulated_ev_mean"] = simulated_ev.mean(axis=1)
    summary["simulated_ev_median"] = ev_p50
    summary["simulated_ev_p05"] = ev_p05
    summary["simulated_ev_p95"] = ev_p95
    summary["prob_ev_negative"] = (simulated_ev < 0).mean(axis=1)
    summary["ev_expected_shortfall_5pct"] = expected_shortfall(simulated_ev, alpha=tail_alpha)

    summary["ev_mean_minus_point_estimate"] = summary["simulated_ev_mean"] - summary["expected_value"]
    summary["ev_p05_minus_point_estimate"] = summary["simulated_ev_p05"] - summary["expected_value"]

    return summary


def run_uncertainty_analysis(
    best_offers_df: pd.DataFrame,
    config: UncertaintyConfig | None = None,
) -> pd.DataFrame:
    if config is None:
        config = UncertaintyConfig()

    validate_input_columns(best_offers_df)

    df = best_offers_df.copy()

    df["adjusted_p_default"] = clip_probabilities(df["adjusted_p_default"])
    df["p_accept"] = clip_probabilities(df["p_accept"])

    rng = np.random.default_rng(config.random_seed)

    pd_alpha, pd_beta = beta_parameterize_from_mean(
        mean=df["adjusted_p_default"],
        concentration=config.probability_concentration,
    )
    accept_alpha, accept_beta = beta_parameterize_from_mean(
        mean=df["p_accept"],
        concentration=config.probability_concentration,
    )

    simulated_pd = simulate_beta_draws(
        alpha=pd_alpha,
        beta=pd_beta,
        n_simulations=config.n_simulations,
        rng=rng,
    )
    simulated_accept = simulate_beta_draws(
        alpha=accept_alpha,
        beta=accept_beta,
        n_simulations=config.n_simulations,
        rng=rng,
    )


    is_no_offer = df["offer_name"] == "no_offer"

    # Force no_offer to zero-risk baseline
    simulated_pd[is_no_offer.values, :] = 0.0
    simulated_accept[is_no_offer.values, :] = 0.0

    simulated_ev = compute_simulated_ev(
        p_default_draws=simulated_pd,
        p_accept_draws=simulated_accept,
        expected_revenue=df["expected_revenue"].to_numpy(dtype=float),
        expected_loss=df["expected_loss"].to_numpy(dtype=float),
    )

    summary = summarize_uncertainty(
        df=df,
        simulated_pd=simulated_pd,
        simulated_accept=simulated_accept,
        simulated_ev=simulated_ev,
        tail_alpha=config.tail_alpha,
    )

    return summary