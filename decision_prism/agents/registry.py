"""Agent Registry — keyword-based domain matching and top-N selection."""

from collections import Counter

from decision_prism.models.domain import DOMAIN_KEYWORDS, dispatch_agents


class AgentRegistry:
    """Match query to domains and select top-N experts with unique stances."""

    def __init__(self, top_n: int = 3):
        self.top_n = top_n
        self._domains = {k: set(v) for k, v in DOMAIN_KEYWORDS.items()}
        self._stances = [
            "government_regulator",
            "enterprise_market",
            "individual_user",
        ]

    def match(self, query: str) -> list[dict]:
        """Return top-N expert assignments with domain, name, and stance."""
        words = set(query.lower().split())
        scores = {}

        for domain, keywords in self._domains.items():
            overlap = len(words & keywords)
            if overlap > 0:
                scores[domain] = overlap

        if not scores:
            # 回退：默认使用 macro_finance
            scores = {"macro_finance": 1}

        sorted_domains = sorted(scores.items(), key=lambda x: -x[1])
        top = sorted_domains[: self.top_n]

        results = []
        for i, (domain, score) in enumerate(top):
            stance = self._stances[i % len(self._stances)]
            domain_name = domain.replace("_", " ").title()
            results.append(
                {
                    "name": f"{domain_name} Expert",
                    "domain": domain,
                    "stance": stance,
                    "score": score,
                }
            )

        return results

    @staticmethod
    def get_available_domains() -> list[str]:
        """Return all supported domain names."""
        return list(DOMAIN_KEYWORDS.keys())

    @staticmethod
    def get_stances() -> list[str]:
        """Return all supported debate stances."""
        return [
            "government_regulator",
            "enterprise_market",
            "individual_user",
        ]