"""Tests for Bayesian Monte Carlo analysis."""

from decision_prism.analysis.bayesian import monte_carlo_simulation


class TestMonteCarlo:
    def test_basic_simulation(self):
        distributions = [("Test Claim", 0.3, 0.5, 0.7)]
        result = monte_carlo_simulation(distributions, n_simulations=10000, seed=42)
        assert "Test Claim" in result
        assert (
            0.3
            <= result["Test Claim"]["p5"]
            <= result["Test Claim"]["p50"]
            <= result["Test Claim"]["p95"]
            <= 0.7
        )

    def test_seed_reproducibility(self):
        distributions = [("Claim", 0.1, 0.5, 0.9)]
        r1 = monte_carlo_simulation(distributions, seed=42)
        r2 = monte_carlo_simulation(distributions, seed=42)
        assert r1["Claim"]["mean"] == r2["Claim"]["mean"]

    def test_percentile_ordering(self):
        distributions = [("X", 10, 50, 90)]
        result = monte_carlo_simulation(distributions, seed=42)
        assert result["X"]["p5"] < result["X"]["p50"] < result["X"]["p95"]

    def test_multiple_distributions(self):
        distributions = [
            ("A", 0.1, 0.3, 0.5),
            ("B", 0.5, 0.7, 0.9),
        ]
        result = monte_carlo_simulation(distributions, seed=42)
        assert "A" in result
        assert "B" in result
        # B should have higher mean than A
        assert result["B"]["mean"] > result["A"]["mean"]
