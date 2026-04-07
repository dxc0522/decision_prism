"""Sentiment analysis from search results (search-based MVP)."""

import re


def analyze_sentiment(search_results: list[dict]) -> dict:
    """Extract a rough sentiment signal from search result content.

    Uses keyword-level heuristics as MVP. Replace with proper
    NLP sentiment analysis when available.

    Args:
        search_results: List of dicts with 'title', 'url', 'content'.

    Returns:
        Dict with sentiment score (-1 to +1) and summary.
    """
    positive_words = [
        "growth",
        "positive",
        "improve",
        "gain",
        "strong",
        "opportunity",
        "benefit",
        "advantage",
        "progress",
        "success",
        "rise",
        "optimistic",
    ]
    negative_words = [
        "decline",
        "negative",
        "crisis",
        "risk",
        "loss",
        "threat",
        "crash",
        "unemployment",
        "debt",
        "recession",
        "fear",
        "collapse",
    ]

    text = " ".join(f"{r.get('title', '')} {r.get('content', '')}" for r in search_results).lower()

    pos_count = sum(len(re.findall(rf"\b{w}\b", text)) for w in positive_words)
    neg_count = sum(len(re.findall(rf"\b{w}\b", text)) for w in negative_words)
    total = pos_count + neg_count

    if total == 0:
        return {"score": 0.0, "label": "neutral", "summary": "No sentiment signal detected"}

    score = (pos_count - neg_count) / total
    label = "positive" if score > 0.15 else ("negative" if score < -0.15 else "neutral")

    return {
        "score": round(score, 3),
        "label": label,
        "summary": (f"Sentiment {label} (pos: {pos_count}, neg: {neg_count}, total: {total})"),
    }
