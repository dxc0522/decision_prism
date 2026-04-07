"""Firecrawl content extraction tests."""


from decision_prism.tools.firecrawl import extract_document


def test_extract_document_import():
    """Verify firecrawl module imports correctly."""
    assert callable(extract_document)


def test_extract_document_has_retry():
    """Verify the function has retry decorator (3 attempts)."""

    # 函数应配置重试机制
    assert hasattr(extract_document, "retry")
