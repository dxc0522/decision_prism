"""Firecrawl content extraction."""

from firecrawl import FirecrawlApp
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def extract_document(url: str, api_key: str) -> str:
    """Extract content from a URL using Firecrawl."""
    app = FirecrawlApp(api_key=api_key)
    response = app.scrape_url(url, {"formats": ["markdown"]})
    return response.get("markdown", "")
