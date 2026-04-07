"""Bayesian calibration via Monte Carlo simulation."""

import numpy as np


def monte_carlo_simulation(
    distributions: list[tuple[str, float, float, float]],
    n_simulations: int = 10000,
    seed: int | None = 42,
) -> dict:
    """Run Monte Carlo simulation over triangular distributions.

    Args:
        distributions: List of (name, low, mode, high) tuples.
        n_simulations: Number of simulation iterations.
        seed: Random seed for reproducibility.

    Returns:
        Dict with mean, std, p5, p50, p95 per distribution.
    """
    rng = np.random.default_rng(seed)
    result: dict[str, dict] = {}

    for name, low, mode, high in distributions:
        samples = rng.triangular(left=low, mode=mode, right=high, size=n_simulations)
        result[name] = {
            "mean": float(np.mean(samples)),
            "std": float(np.std(samples)),
            "p5": float(np.percentile(samples, 5)),
            "p50": float(np.percentile(samples, 50)),
            "p95": float(np.percentile(samples, 95)),
        }

    return result
