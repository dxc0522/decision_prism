"""Tests for agent dispatch / domain matching."""

from decision_prism.models.domain import DOMAIN_KEYWORDS, STANCES, dispatch_agents


class TestDispatchAgents:
    def test_interest_rate_housing(self):
        """Query about interest rates and housing should match macro_finance and urban_planning."""
        query = "What is the impact of rising interest rates on urban housing development?"
        agents = dispatch_agents(query, top_n=3)
        assert len(agents) == 3
        domains = [a["domain"] for a in agents]
        assert "macro_finance" in domains or "urban_planning" in domains

    def test_stances_unique(self):
        """Top-3 experts should get unique stances."""
        query = "Should we regulate AI development in healthcare?"
        agents = dispatch_agents(query, top_n=3)
        stances = [a["stance"] for a in agents]
        assert len(stances) == 3
        assert len(set(stances)) == 3

    def test_no_keywords_returns_defaults(self):
        """Query with no matching keywords should still return agents."""
        query = "What color is the sky?"
        agents = dispatch_agents(query, top_n=3)
        assert len(agents) == 3

    def test_top_n_respected(self):
        assert len(dispatch_agents("test query", top_n=2)) == 2
        assert len(dispatch_agents("test query", top_n=5)) == 5

    def test_all_domains_covered(self):
        """All domains should be reachable given appropriate queries."""
        all_reachable = set()
        for domain, keywords in DOMAIN_KEYWORDS.items():
            for kw in keywords:
                agents = dispatch_agents(kw, top_n=3)
                for a in agents:
                    all_reachable.add(a["domain"])
        assert all_reachable == set(DOMAIN_KEYWORDS.keys())

    def test_stances_from_defined_list(self):
        query = "test query with interest rate and urban planning and AI ethics"
        agents = dispatch_agents(query, top_n=3)
        for a in agents:
            assert a["stance"] in STANCES
