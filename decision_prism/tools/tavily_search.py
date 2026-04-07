"""Tavily AI search integration."""

from tavily import TavilyClient
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def tavily_search(query: str, api_key: str, num_results: int = 5) -> list[dict]:
    """Search Tavily and return results with title, url, and content."""
    client = TavilyClient(api_key=api_key)
    response = client.search(query=query, max_results=num_results)
    return [
        {"title": r.get("title", ""), "url": r.get("url", ""), "content": r.get("content", "")}
        for r in response.get("results", [])
    ]
