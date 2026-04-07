"""Sentiment analysis tests."""

from decision_prism.tools.sentiment import analyze_sentiment


def test_positive_sentiment():
    results = [
        {
            "title": "Growth in housing",
            "content": "Strong growth and positive outlook. Benefits and progress reported.",
        }
    ]
    result = analyze_sentiment(results)
    assert result["label"] == "positive"
    assert result["score"] > 0.15


def test_negative_sentiment():
    results = [
        {
            "title": "Market decline",
            "content": "Crisis and risk of collapse. Recession fears and debt concerns grow.",
        }
    ]
    result = analyze_sentiment(results)
    assert result["label"] == "negative"
    assert result["score"] < -0.15


def test_neutral_sentiment():
    results = [
        {
            "title": "Market update",
            "content": "The situation remains unchanged. No significant movement.",
        }
    ]
    result = analyze_sentiment(results)
    assert result["label"] == "neutral"
    assert result["score"] == 0.0


def test_empty_results():
    result = analyze_sentiment([])
    assert result["label"] == "neutral"
    assert result["score"] == 0.0
    assert "No sentiment" in result["summary"]


def test_mixed_sentiment():
    results = [
        {
            "title": "Growth report",
            "content": "Growth and positive trends. However, risk and debt concerns persist.",
        }
    ]
    result = analyze_sentiment(results)
    assert result["label"] in ("positive", "negative", "neutral")


def test_missing_fields_in_results():
    results = [{"title": "No content key"}]
    result = analyze_sentiment(results)
    assert isinstance(result["score"], float)


def test_score_rounding():
    results = [
        {
            "title": "Success story",
            "content": "growth positive improve gain strong opportunity "
            "benefit advantage progress success rise optimistic",
        }
    ]
    result = analyze_sentiment(results)
    assert result["score"] == round(result["score"], 3)
