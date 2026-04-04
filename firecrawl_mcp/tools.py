"""Firecrawl MCP Server tools.

All tenant-facing tools require api_key parameter for stateless multi-tenancy.
Health check is unauthenticated as it doesn't access tenant data.
"""

import json
import logging
from typing import Any, Dict

from fastmcp import FastMCP
from pydantic import Field

from .service import make_firecrawl_request

logger = logging.getLogger("firecrawl-mcp-server")


def register_tools(mcp: FastMCP) -> None:
    """Register all Firecrawl tools with the MCP server."""

    @mcp.tool(
        name="health_check",
        description="Check server readiness and basic connectivity. No authentication required.",
    )
    def health_check() -> str:
        """Diagnostic tool to verify server is operational.

        Returns:
            JSON string with server status
        """
        return json.dumps(
            {
                "success": True,
                "status": "ok",
                "server": "CL Firecrawl MCP Server",
                "version": "0.1.0",
            }
        )

    @mcp.tool(
        name="scrape",
        description="Scrape a single URL and extract content in multiple formats.",
    )
    def scrape(
        api_key: str = Field(..., description="Firecrawl API key for authentication"),
        url: str = Field(..., description="The URL to scrape"),
        formats: str = Field(
            default="markdown",
            description="Output formats (comma-separated): markdown, html, rawHtml, json, screenshot, links, images, summary, audio, branding, changeTracking",
        ),
        only_main_content: bool = Field(
            default=True,
            description="Extract only main content, excluding headers/footers/navs",
        ),
        include_tags: str | None = Field(
            None,
            description="Comma-separated HTML tags to include in output",
        ),
        exclude_tags: str | None = Field(
            None,
            description="Comma-separated HTML tags to exclude from output",
        ),
        wait_for_selector: str | None = Field(
            None,
            description="CSS selector to wait for before scraping",
        ),
        timeout_ms: int = Field(
            default=30000,
            description="Request timeout in milliseconds (1000-300000)",
        ),
        mobile: bool = Field(
            default=False,
            description="Emulate mobile device (responsive layout)",
        ),
        skip_tls_verification: bool = Field(
            default=True,
            description="Skip TLS certificate verification",
        ),
        proxy: str = Field(
            default="auto",
            description="Proxy type: basic, enhanced, or auto",
        ),
        block_ads: bool = Field(
            default=True,
            description="Block ads and cookie popups",
        ),
        remove_base64_images: bool = Field(
            default=True,
            description="Remove base64 encoded images from markdown",
        ),
    ) -> str:
        """Scrape a URL using Firecrawl API with flexible format support.

        Extracts content in multiple formats with options for filtering,
        timeouts, and browser emulation.

        Args:
            api_key: API authentication key
            url: Target URL
            formats: Output formats (comma-separated list)
            only_main_content: Filter to main page content
            include_tags: HTML tags to include
            exclude_tags: HTML tags to exclude
            wait_for_selector: CSS selector to wait for
            timeout_ms: Timeout in milliseconds
            mobile: Mobile device emulation
            skip_tls_verification: Skip TLS checks
            proxy: Proxy strategy
            block_ads: Ad/popup blocking
            remove_base64_images: Remove base64 images

        Returns:
            JSON string with scraped data or error
        """
        # Validate timeout
        if timeout_ms < 1000 or timeout_ms > 300000:
            return json.dumps(
                {
                    "success": False,
                    "error": "Timeout must be 1000-300000 ms",
                    "statusCode": 400,
                    "message": "Invalid timeout",
                    "details": {},
                }
            )

        # Parse formats from comma-separated string
        format_list = [f.strip() for f in formats.split(",") if f.strip()]
        formats_array = [{"type": fmt} for fmt in format_list]

        # Build base request body
        body = {
            "url": url,
            "formats": formats_array,
            "onlyMainContent": only_main_content,
            "timeout": timeout_ms,
            "mobile": mobile,
            "skipTlsVerification": skip_tls_verification,
            "proxy": proxy,
            "blockAds": block_ads,
            "removeBase64Images": remove_base64_images,
        }

        # Add include/exclude tags if provided
        if include_tags:
            body["includeTags"] = [t.strip() for t in include_tags.split(",")]
        if exclude_tags:
            body["excludeTags"] = [t.strip() for t in exclude_tags.split(",")]

        # Add wait action if selector provided
        if wait_for_selector:
            body["actions"] = [
                {
                    "type": "wait",
                    "selector": wait_for_selector,
                }
            ]

        result = make_firecrawl_request(
            method="POST",
            endpoint="/scrape",
            api_key=api_key,
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="crawl",
        description="Crawl an entire website and extract content from all pages.",
    )
    def crawl(
        api_key: str = Field(..., description="Firecrawl API key"),
        url: str = Field(..., description="Root URL of website to crawl"),
        max_depth: int = Field(
            default=2,
            description="Maximum depth to crawl (0-10)",
        ),
        limit: int = Field(
            default=100,
            description="Maximum number of pages to crawl",
        ),
        format: str = Field(
            default="markdown",
            description="Output format: 'markdown' or 'json'",
        ),
    ) -> str:
        """Crawl a website and extract content from multiple pages.

        Args:
            api_key: Firecrawl API authentication key
            url: Root URL to start crawling
            max_depth: Maximum depth to crawl
            limit: Maximum pages to crawl
            format: Output format

        Returns:
            JSON string with crawl results or error
        """
        body = {
            "url": url,
            "maxDepth": max_depth,
            "limit": limit,
            "scrapeOptions": {
                "formats": [format],
            },
        }

        result = make_firecrawl_request(
            method="POST",
            endpoint="/crawl",
            api_key=api_key,
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="map",
        description="Get a list of all URLs from a website without scraping content.",
    )
    def map(
        api_key: str = Field(..., description="Firecrawl API key"),
        url: str = Field(..., description="Root URL to map"),
        limit: int = Field(
            default=10000,
            description="Maximum URLs to return",
        ),
    ) -> str:
        """Map all URLs on a website.

        Args:
            api_key: Firecrawl API authentication key
            url: Root URL to map
            limit: Maximum URLs to return

        Returns:
            JSON string with URL list or error
        """
        body = {
            "url": url,
            "limit": limit,
        }

        result = make_firecrawl_request(
            method="POST",
            endpoint="/map",
            api_key=api_key,
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="search",
        description="Search the web and retrieve full page content for results.",
    )
    def search(
        api_key: str = Field(..., description="Firecrawl API key"),
        query: str = Field(..., description="Search query"),
        limit: int = Field(
            default=10,
            description="Maximum results to return",
        ),
        format: str = Field(
            default="markdown",
            description="Output format: 'markdown' or 'json'",
        ),
    ) -> str:
        """Search the web and get full content from results.

        Args:
            api_key: Firecrawl API authentication key
            query: Search query
            limit: Maximum results
            format: Output format

        Returns:
            JSON string with search results or error
        """
        body = {
            "query": query,
            "limit": limit,
            "scrapeOptions": {
                "formats": [format],
            },
        }

        result = make_firecrawl_request(
            method="POST",
            endpoint="/search",
            api_key=api_key,
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="extract",
        description="Extract structured data from a webpage using a JSON schema.",
    )
    def extract(
        api_key: str = Field(..., description="Firecrawl API key"),
        url: str = Field(..., description="URL to extract from"),
        schema: str = Field(
            ...,
            description="JSON schema definition for structured extraction",
        ),
        mode: str = Field(
            default="llm-extraction",
            description="Extraction mode: 'llm-extraction' or 'fast'",
        ),
    ) -> str:
        """Extract structured data from a webpage using a schema.

        Args:
            api_key: Firecrawl API authentication key
            url: Target URL
            schema: JSON schema for desired output structure
            mode: Extraction mode

        Returns:
            JSON string with extracted data or error
        """
        try:
            schema_dict = json.loads(schema)
        except json.JSONDecodeError as e:
            error_response = {
                "success": False,
                "error": f"Invalid JSON schema: {str(e)}",
                "statusCode": 400,
                "message": "Schema must be valid JSON",
                "details": {},
            }
            return json.dumps(error_response)

        body = {
            "url": url,
            "schema": schema_dict,
            "mode": mode,
        }

        result = make_firecrawl_request(
            method="POST",
            endpoint="/extract",
            api_key=api_key,
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="agent",
        description="Autonomously navigate and interact with websites to complete tasks.",
    )
    def agent(
        api_key: str = Field(..., description="Firecrawl API key"),
        url: str = Field(..., description="Starting URL for agent navigation"),
        objective: str = Field(
            ...,
            description="Task or objective for the agent to complete",
        ),
        max_iterations: int = Field(
            default=10,
            description="Maximum iterations/steps (1-20)",
        ),
    ) -> str:
        """Use an autonomous agent to navigate and complete tasks.

        Args:
            api_key: Firecrawl API authentication key
            url: Starting URL
            objective: Task for the agent
            max_iterations: Maximum steps to take

        Returns:
            JSON string with agent results or error
        """
        body = {
            "url": url,
            "objective": objective,
            "maxIterations": max_iterations,
        }

        result = make_firecrawl_request(
            method="POST",
            endpoint="/agent",
            api_key=api_key,
            body=body,
        )

        return json.dumps(result)
