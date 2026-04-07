"""Domain definitions and keyword-based expert dispatching."""

from collections import Counter

DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "urban_planning": [
        "city",
        "urban",
        "zoning",
        "infrastructure",
        "transport",
        "housing",
        "development",
        "planning",
        "real estate",
        "property",
    ],
    "macro_finance": [
        "economy",
        "gdp",
        "inflation",
        "interest rate",
        "monetary",
        "fiscal",
        "market",
        "stock",
        "bank",
        "financial",
        "trade",
        "investment",
    ],
    "demographics": [
        "population",
        "birth rate",
        "aging",
        "migration",
        "census",
        "demographic",
        "youth",
        "workforce",
        "employment",
    ],
    "industrial_eco": [
        "industry",
        "supply chain",
        "manufacturing",
        "industrial policy",
        "sector",
        "production",
        "factory",
        "semiconductor",
        "tech industry",
    ],
    "legal_compliance": [
        "regulation",
        "law",
        "compliance",
        "legal",
        "policy",
        "statute",
        "legislation",
        "governance",
        "tax",
        "tariff",
        "sanction",
    ],
    "tech_ethics": [
        "ai",
        "privacy",
        "ethics",
        "surveillance",
        "algorithmic",
        "bias",
        "data",
        "cybersecurity",
        "digital",
        "technology",
    ],
    "energy_environment": [
        "energy",
        "carbon",
        "climate",
        "environment",
        "renewable",
        "solar",
        "wind",
        "nuclear",
        "emission",
        "pollution",
    ],
    "social_stability": [
        "social",
        "protest",
        "stability",
        "public opinion",
        "sentiment",
        "inequality",
        "unrest",
        "polarization",
        "trust",
    ],
}

STANCES = ["government_regulator", "enterprise_market", "individual_user"]


def dispatch_agents(query: str, top_n: int = 3) -> list[dict]:
    """Select top-N domain experts from a keyword-based scoring system.

    Args:
        query: User's natural language query (pre-lowercased).
        top_n: Number of experts to select.

    Returns:
        List of dicts with keys: name, domain, stance.
    """
    query_lower = query.lower()
    words = query_lower.split()

    scores: Counter = Counter()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in query_lower:
                scores[domain] += 2
            for word in words:
                if kw.startswith(word) or word.startswith(kw):
                    scores[domain] += 1

    top_domains = [d for d, _ in scores.most_common(top_n)]

    if len(top_domains) < top_n:
        all_domains = list(DOMAIN_KEYWORDS.keys())
        for d in all_domains:
            if d not in top_domains:
                top_domains.append(d)
                if len(top_domains) == top_n:
                    break

    assigned: list[dict] = []
    for i, domain in enumerate(top_domains):
        stance = STANCES[i % len(STANCES)]
        assigned.append(
            {
                "name": f"{domain.replace('_', ' ').title()} Expert",
                "domain": domain,
                "stance": stance,
            }
        )
    return assigned
