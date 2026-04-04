"""Schemas and type definitions for Firecrawl MCP Server."""

from typing_extensions import TypedDict


class FirecrawlAPIKeyData(TypedDict, total=False):
    """Firecrawl API key authentication data."""

    api_key: str


class ScrapeParams(TypedDict, total=False):
    """Parameters for scrape operations."""

    url: str
    formats: list[str]
    headers: dict
    timeout: int


class CrawlParams(TypedDict, total=False):
    """Parameters for crawl operations."""

    url: str
    limit: int
    maxDepth: int
    scrapeOptions: dict


class SearchParams(TypedDict, total=False):
    """Parameters for search operations."""

    query: str
    limit: int


class ExtractParams(TypedDict, total=False):
    """Parameters for extract operations."""

    url: str
    schema: dict
    mode: str
