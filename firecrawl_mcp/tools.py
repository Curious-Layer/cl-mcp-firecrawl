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
        description="Crawl multiple URLs and extract content based on specified options.",
    )
    def crawl(
        api_key: str = Field(..., description="Firecrawl API key for authentication"),
        url: str = Field(..., description="The base URL to start crawling from"),
        prompt: str | None = Field(
            None,
            description="Natural language prompt to generate crawler options",
        ),
        exclude_paths: str | None = Field(
            None,
            description="Comma-separated regex patterns for URLs to exclude",
        ),
        include_paths: str | None = Field(
            None,
            description="Comma-separated regex patterns for URLs to include",
        ),
        max_discovery_depth: int | None = Field(
            None,
            description="Maximum depth based on discovery order",
        ),
        sitemap: str = Field(
            default="include",
            description="Sitemap mode: skip, include, or only",
        ),
        ignore_query_parameters: bool = Field(
            default=False,
            description="Don't re-scrape same path with different query parameters",
        ),
        regex_on_full_url: bool = Field(
            default=False,
            description="Match patterns against full URL including query parameters",
        ),
        limit: int = Field(
            default=10000,
            description="Maximum number of pages to crawl",
        ),
        crawl_entire_domain: bool = Field(
            default=False,
            description="Follow sibling and parent URLs, not just child paths",
        ),
        allow_external_links: bool = Field(
            default=False,
            description="Allow crawler to follow external links",
        ),
        allow_subdomains: bool = Field(
            default=False,
            description="Allow crawler to follow subdomains",
        ),
        delay: float | None = Field(
            None,
            description="Delay in seconds between scrapes",
        ),
        max_concurrency: int | None = Field(
            None,
            description="Maximum concurrent scrapes",
        ),
        formats: str = Field(
            default="markdown",
            description="Output formats (comma-separated): markdown, html, rawHtml, json, screenshot, links, images, summary, audio, branding, changeTracking",
        ),
        only_main_content: bool = Field(
            default=True,
            description="Extract only main content, excluding headers/footers",
        ),
        include_tags: str | None = Field(
            None,
            description="Comma-separated HTML tags to include",
        ),
        exclude_tags: str | None = Field(
            None,
            description="Comma-separated HTML tags to exclude",
        ),
        wait_for_selector: str | None = Field(
            None,
            description="CSS selector to wait for before scraping",
        ),
        mobile: bool = Field(
            default=False,
            description="Emulate mobile device",
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
            description="Remove base64 encoded images",
        ),
        zero_data_retention: bool = Field(
            default=False,
            description="Enable zero data retention",
        ),
    ) -> str:
        """Crawl a website starting from a base URL with flexible options.

        Supports URL filtering, sitemap control, concurrency management,
        and full scraping options for each page.

        Args:
            api_key: API authentication key
            url: Base URL to start crawling
            prompt: Natural language crawler options
            exclude_paths: Regex patterns for URLs to exclude
            include_paths: Regex patterns for URLs to include
            max_discovery_depth: Maximum discovery depth
            sitemap: skip, include, or only
            ignore_query_parameters: Ignore different query parameters
            regex_on_full_url: Match patterns on full URL
            limit: Maximum pages to crawl
            crawl_entire_domain: Follow siblings and parents
            allow_external_links: Allow external links
            allow_subdomains: Allow subdomains
            delay: Delay between scrapes in seconds
            max_concurrency: Max concurrent scrapes
            formats: Output formats (comma-separated)
            only_main_content: Extract main content only
            include_tags: HTML tags to include
            exclude_tags: HTML tags to exclude
            wait_for_selector: CSS selector to wait for
            mobile: Mobile device emulation
            skip_tls_verification: Skip TLS checks
            proxy: Proxy strategy
            block_ads: Ad/popup blocking
            remove_base64_images: Remove base64 images
            zero_data_retention: Enable zero data retention

        Returns:
            JSON string with crawl job info or error
        """
        # Build base request body
        body = {
            "url": url,
            "sitemap": sitemap,
            "ignoreQueryParameters": ignore_query_parameters,
            "regexOnFullURL": regex_on_full_url,
            "limit": limit,
            "crawlEntireDomain": crawl_entire_domain,
            "allowExternalLinks": allow_external_links,
            "allowSubdomains": allow_subdomains,
            "zeroDataRetention": zero_data_retention,
        }

        # Add optional prompt parameter
        if prompt:
            body["prompt"] = prompt

        # Add path patterns if provided
        if exclude_paths:
            body["excludePaths"] = [p.strip() for p in exclude_paths.split(",")]
        if include_paths:
            body["includePaths"] = [p.strip() for p in include_paths.split(",")]

        # Add optional discovery depth
        if max_discovery_depth is not None:
            body["maxDiscoveryDepth"] = max_discovery_depth

        # Add optional delay and concurrency
        if delay is not None:
            body["delay"] = delay
        if max_concurrency is not None:
            body["maxConcurrency"] = max_concurrency

        # Build scrapeOptions
        format_list = [f.strip() for f in formats.split(",") if f.strip()]
        formats_array = [{"type": fmt} for fmt in format_list]

        scrape_options = {
            "formats": formats_array,
            "onlyMainContent": only_main_content,
            "blockAds": block_ads,
            "removeBase64Images": remove_base64_images,
        }

        if mobile:
            scrape_options["mobile"] = mobile
        if skip_tls_verification:
            scrape_options["skipTlsVerification"] = skip_tls_verification
        if proxy:
            scrape_options["proxy"] = proxy

        # Add include/exclude tags if provided
        if include_tags:
            scrape_options["includeTags"] = [t.strip() for t in include_tags.split(",")]
        if exclude_tags:
            scrape_options["excludeTags"] = [t.strip() for t in exclude_tags.split(",")]

        # Add wait action if selector provided
        if wait_for_selector:
            scrape_options["actions"] = [
                {
                    "type": "wait",
                    "selector": wait_for_selector,
                }
            ]

        body["scrapeOptions"] = scrape_options

        result = make_firecrawl_request(
            method="POST",
            endpoint="/crawl",
            api_key=api_key,
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="map",
        description="Map all URLs on a website with optional filtering and search.",
    )
    def map(
        api_key: str = Field(..., description="Firecrawl API key for authentication"),
        url: str = Field(..., description="The base URL to start mapping from"),
        search: str | None = Field(
            None,
            description="Search query to filter and order results by relevance",
        ),
        sitemap: str = Field(
            default="include",
            description="Sitemap mode: skip, include, or only",
        ),
        include_subdomains: bool = Field(
            default=True,
            description="Include subdomains of the website",
        ),
        ignore_query_parameters: bool = Field(
            default=True,
            description="Don't return URLs with query parameters",
        ),
        ignore_cache: bool = Field(
            default=False,
            description="Bypass sitemap cache to get fresh URLs",
        ),
        limit: int = Field(
            default=5000,
            description="Maximum number of URLs to return (max 100000)",
        ),
        timeout_ms: int | None = Field(
            None,
            description="Timeout in milliseconds",
        ),
        country: str | None = Field(
            None,
            description="ISO 3166-1 alpha-2 country code (e.g., US, DE, JP)",
        ),
        languages: str | None = Field(
            None,
            description="Comma-separated preferred languages (e.g., en-US,de-DE)",
        ),
    ) -> str:
        """Map all URLs on a website.

        Discovers and lists all URLs found on a website with optional
        filtering by search query, subdomain inclusion, and location settings.

        Args:
            api_key: API authentication key
            url: Base URL to start mapping
            search: Query to filter and order results
            sitemap: skip, include, or only
            include_subdomains: Include subdomains
            ignore_query_parameters: Skip query parameter URLs
            ignore_cache: Bypass sitemap cache
            limit: Maximum URLs to return
            timeout_ms: Timeout in milliseconds
            country: ISO country code for location
            languages: Comma-separated language codes

        Returns:
            JSON string with mapped URLs or error
        """
        # Validate limit
        if limit > 100000:
            return json.dumps(
                {
                    "success": False,
                    "error": "Limit must be 100000 or less",
                    "statusCode": 400,
                    "message": "Invalid limit",
                    "details": {},
                }
            )

        # Build base request body
        body = {
            "url": url,
            "sitemap": sitemap,
            "includeSubdomains": include_subdomains,
            "ignoreQueryParameters": ignore_query_parameters,
            "ignoreCache": ignore_cache,
            "limit": limit,
        }

        # Add optional search parameter
        if search:
            body["search"] = search

        # Add optional timeout
        if timeout_ms is not None:
            body["timeout"] = timeout_ms

        # Build location object if country or languages provided
        if country or languages:
            location = {}
            if country:
                location["country"] = country
            if languages:
                location["languages"] = [lang.strip() for lang in languages.split(",")]
            body["location"] = location

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
