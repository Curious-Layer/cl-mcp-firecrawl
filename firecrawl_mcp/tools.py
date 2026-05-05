"""Firecrawl MCP Server tools.

Credentials are injected server-side via fastmcp-credentials middleware.
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
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="crawl",
        description="Crawl multiple URLs and extract content based on specified options.",
    )
    def crawl(
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
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="map",
        description="Map all URLs on a website with optional filtering and search.",
    )
    def map(
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
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="search",
        description="Search the web and optionally scrape search results with advanced filtering options.",
    )
    def search(
        query: str = Field(
            ..., description="Search query (max 500 characters)", max_length=500
        ),
        limit: int = Field(
            default=5,
            description="Maximum number of results to return (1-100)",
            ge=1,
            le=100,
        ),
        sources: str = Field(
            default="web",
            description="Search sources (comma-separated): web, images, news. Default: web",
        ),
        categories: str | None = Field(
            None,
            description="Filter by categories (comma-separated): github, research, pdf",
        ),
        tbs: str | None = Field(
            None,
            description="Time-based search filter (e.g., 'qdr:d' for past day, 'qdr:w' for past week, 'qdr:m' for past month)",
        ),
        location: str | None = Field(
            None,
            description="Geographic location for search results (e.g., 'San Francisco,California,United States')",
        ),
        country: str | None = Field(
            None,
            description="ISO country code for geo-targeting (e.g., 'US', 'DE', 'FR', 'JP'). Default: 'US'",
        ),
        timeout: int = Field(
            default=60000,
            description="Timeout in milliseconds (default: 60000)",
            ge=1000,
            le=300000,
        ),
        ignore_invalid_urls: bool = Field(
            default=False,
            description="Exclude invalid URLs from search results",
        ),
        enterprise: str | None = Field(
            None,
            description="Enterprise search options (comma-separated): anon, zdr. For Zero Data Retention (ZDR)",
        ),
        formats: str = Field(
            default="markdown",
            description="Scrape output formats (comma-separated): markdown, html, rawHtml, json, screenshot, links, images, summary, audio, branding",
        ),
        mobile: bool = Field(
            default=False,
            description="Emulate mobile device when scraping results",
        ),
        proxy: str = Field(
            default="auto",
            description="Proxy type: basic, enhanced, auto",
        ),
        block_ads: bool = Field(
            default=True,
            description="Enable ad-blocking and cookie popup blocking",
        ),
    ) -> str:
        """Search the web and optionally extract full content from results.

        Args:
            query: Search query string
            limit: Max results (1-100)
            sources: Search sources (web, images, news)
            categories: Filter by categories (github, research, pdf)
            tbs: Time-based search filter
            location: Geographic location for results
            country: ISO country code
            timeout: Request timeout in milliseconds
            ignore_invalid_urls: Exclude invalid URLs
            enterprise: Enterprise search options (anon, zdr)
            formats: Scrape output formats
            mobile: Emulate mobile device
            proxy: Proxy type
            block_ads: Enable ad blocking

        Returns:
            JSON string with search results or error
        """
        # Validate limit range
        if limit < 1 or limit > 100:
            return json.dumps(
                {
                    "success": False,
                    "error": "Limit must be between 1 and 100",
                    "statusCode": 400,
                }
            )

        # Validate timeout range
        if timeout < 1000 or timeout > 300000:
            return json.dumps(
                {
                    "success": False,
                    "error": "Timeout must be between 1000 and 300000 milliseconds",
                    "statusCode": 400,
                }
            )

        # Parse comma-separated sources and build sources array
        sources_list = [s.strip() for s in sources.split(",") if s.strip()]
        sources_array = []
        for source in sources_list:
            source_obj = {"type": source}
            # Add tbs and location to web source if provided
            if source == "web":
                if tbs:
                    source_obj["tbs"] = tbs
                if location:
                    source_obj["location"] = location
            sources_array.append(source_obj)

        # Parse comma-separated categories
        categories_list = []
        if categories:
            categories_list = [
                {"type": c.strip()} for c in categories.split(",") if c.strip()
            ]

        # Parse comma-separated enterprise options
        enterprise_list = []
        if enterprise:
            enterprise_list = [e.strip() for e in enterprise.split(",") if e.strip()]

        format_list = [f.strip() for f in formats.split(",") if f.strip()]
        formats_array = [{"type": fmt} for fmt in format_list]

        body = {
            "query": query,
            "limit": limit,
            "sources": sources_array,
            "timeout": timeout,
            "ignoreInvalidURLs": ignore_invalid_urls,
            "scrapeOptions": {
                "formats": formats_array,
                "mobile": mobile,
                "proxy": proxy,
                "blockAds": block_ads,
            },
        }

        # Add optional parameters if provided
        if tbs and not sources_list:  # If tbs provided but not in sources
            body["tbs"] = tbs
        if location and not sources_list:  # If location provided but not in sources
            body["location"] = location
        if country:
            body["country"] = country
        if categories_list:
            body["categories"] = categories_list
        if enterprise_list:
            body["enterprise"] = enterprise_list

        result = make_firecrawl_request(
            method="POST",
            endpoint="/search",
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="agent",
        description="Autonomously navigate and interact with websites to extract data based on a prompt.",
    )
    def agent(
        prompt: str = Field(
            ...,
            description="Natural language description of data to extract (max 10000 characters)",
            max_length=10000,
        ),
        urls: str | None = Field(
            None,
            description="Optional comma-separated URLs to constrain the agent to",
        ),
        schema: str | None = Field(
            None,
            description="Optional JSON schema to structure the extracted data",
        ),
        max_credits: float | None = Field(
            None,
            description="Maximum credits to spend on this agent task (defaults to 2500)",
        ),
        strict_constrain_to_urls: bool = Field(
            default=False,
            description="If true, agent will only visit URLs provided in the urls parameter",
        ),
        model: str = Field(
            default="spark-1-mini",
            description="Model to use: spark-1-mini (cheaper, default) or spark-1-pro (higher accuracy)",
        ),
    ) -> str:
        """Start an autonomous agent task for data extraction.

        The agent will navigate websites and extract data based on your prompt.
        This is an async operation - the response includes a job ID to check status.

        Args:
            prompt: Description of what data to extract (max 10000 chars)
            urls: Optional comma-separated URLs to constrain agent navigation
            schema: Optional JSON schema for structured output
            max_credits: Maximum credits to spend (default 2500)
            strict_constrain_to_urls: Only visit provided URLs if true
            model: spark-1-mini (default, 60% cheaper) or spark-1-pro (higher accuracy)

        Returns:
            JSON string with agent job ID or error
        """
        # Validate prompt
        if not prompt or len(prompt.strip()) == 0:
            return json.dumps(
                {
                    "success": False,
                    "error": "Prompt is required and cannot be empty",
                    "statusCode": 400,
                }
            )

        # Validate model
        if model not in ["spark-1-mini", "spark-1-pro"]:
            return json.dumps(
                {
                    "success": False,
                    "error": "Model must be 'spark-1-mini' or 'spark-1-pro'",
                    "statusCode": 400,
                }
            )

        # Build request body
        body = {
            "prompt": prompt,
            "model": model,
        }

        # Add optional URLs array if provided
        if urls:
            urls_list = [u.strip() for u in urls.split(",") if u.strip()]
            if urls_list:
                body["urls"] = urls_list

        # Add optional schema if provided
        if schema:
            try:
                schema_dict = json.loads(schema)
                body["schema"] = schema_dict
            except json.JSONDecodeError as e:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid JSON schema: {str(e)}",
                        "statusCode": 400,
                    }
                )

        # Add optional max credits
        if max_credits is not None:
            body["maxCredits"] = max_credits

        # Add strict URL constraint if URLs provided
        if urls and strict_constrain_to_urls:
            body["strictConstrainToURLs"] = True

        result = make_firecrawl_request(
            method="POST",
            endpoint="/agent",
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="agent_status",
        description="Check the status of an agent job and retrieve results when complete.",
    )
    def agent_status(
        job_id: str = Field(
            ...,
            description="The agent job ID returned by the agent tool (UUID format)",
        ),
    ) -> str:
        """Check the status and results of an agent job.

        Agent jobs are asynchronous. Use this to poll for completion.
        Poll every 15-30 seconds and keep polling for at least 2-3 minutes
        before considering the request failed.

        Args:
            job_id: Agent job ID from agent tool response

        Returns:
            JSON string with job status:
            - processing: Agent is still working, keep polling
            - completed: Job finished, response includes extracted data
            - failed: An error occurred during processing
        """
        # Validate job_id is not empty
        if not job_id or len(job_id.strip()) == 0:
            return json.dumps(
                {
                    "success": False,
                    "error": "Job ID is required and cannot be empty",
                    "statusCode": 400,
                }
            )

        # Make GET request to check status
        result = make_firecrawl_request(
            method="GET",
            endpoint=f"/agent/{job_id}",
            body=None,
        )

        return json.dumps(result)

    @mcp.tool(
        name="extract",
        description="Start an async extraction job to extract structured data from URLs using LLMs.",
    )
    def extract(
        urls: str = Field(
            ...,
            description="Comma-separated URLs to extract data from (glob format supported)",
        ),
        prompt: str | None = Field(
            None,
            description="Custom prompt to guide the extraction process",
        ),
        schema: str | None = Field(
            None,
            description="JSON schema to structure the extracted data",
        ),
        enable_web_search: bool = Field(
            default=False,
            description="Use web search to find additional data during extraction",
        ),
        ignore_sitemap: bool = Field(
            default=False,
            description="Ignore sitemap.xml files during website scanning",
        ),
        include_subdomains: bool = Field(
            default=True,
            description="Include subdomains when scanning URLs",
        ),
        show_sources: bool = Field(
            default=False,
            description="Include sources used for extraction in response",
        ),
        ignore_invalid_urls: bool = Field(
            default=True,
            description="Ignore invalid URLs instead of failing entire request",
        ),
        formats: str = Field(
            default="markdown",
            description="Scrape output formats (comma-separated): markdown, html, rawHtml, json, screenshot, links, images, summary, audio, branding",
        ),
        only_main_content: bool = Field(
            default=True,
            description="Extract only main content, excluding headers/footers",
        ),
        mobile: bool = Field(
            default=False,
            description="Emulate mobile device during scraping",
        ),
        proxy: str = Field(
            default="auto",
            description="Proxy type: basic, enhanced, or auto",
        ),
        block_ads: bool = Field(
            default=True,
            description="Enable ad-blocking and cookie popup blocking",
        ),
    ) -> str:
        """Start an async extraction job to extract structured data from URLs.

        This is an async operation - returns a job ID to check status with extract_status.

        Args:
            urls: Comma-separated URLs to extract from (supports glob patterns)
            prompt: Optional prompt to guide extraction
            schema: Optional JSON schema for structured output
            enable_web_search: Use web search for additional data
            ignore_sitemap: Ignore sitemap.xml files
            include_subdomains: Include subdomains in scanning
            show_sources: Include sources in response
            ignore_invalid_urls: Ignore invalid URLs
            formats: Scrape output formats (comma-separated)
            only_main_content: Extract main content only
            mobile: Emulate mobile device
            proxy: Proxy type
            block_ads: Enable ad blocking

        Returns:
            JSON string with extraction job ID or error
        """
        # Validate URLs
        urls_list = [u.strip() for u in urls.split(",") if u.strip()]
        if not urls_list:
            return json.dumps(
                {
                    "success": False,
                    "error": "At least one URL is required",
                    "statusCode": 400,
                }
            )

        body = {
            "urls": urls_list,
            "enableWebSearch": enable_web_search,
            "ignoreSitemap": ignore_sitemap,
            "includeSubdomains": include_subdomains,
            "showSources": show_sources,
            "ignoreInvalidURLs": ignore_invalid_urls,
        }

        # Add optional prompt
        if prompt:
            body["prompt"] = prompt

        # Add optional schema
        if schema:
            try:
                schema_dict = json.loads(schema)
                body["schema"] = schema_dict
            except json.JSONDecodeError as e:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid JSON schema: {str(e)}",
                        "statusCode": 400,
                    }
                )

        format_list = [f.strip() for f in formats.split(",") if f.strip()]
        formats_array = [{"type": fmt} for fmt in format_list]

        scrape_options = {
            "formats": formats_array,
            "onlyMainContent": only_main_content,
            "mobile": mobile,
            "proxy": proxy,
            "blockAds": block_ads,
        }

        body["scrapeOptions"] = scrape_options

        result = make_firecrawl_request(
            method="POST",
            endpoint="/extract",
            body=body,
        )

        return json.dumps(result)

    @mcp.tool(
        name="extract_status",
        description="Check the status of an extraction job and retrieve results when complete.",
    )
    def extract_status(
        job_id: str = Field(
            ...,
            description="The extraction job ID returned by the extract tool (UUID format)",
        ),
    ) -> str:
        """Check the status and results of an extraction job.

        Extraction jobs are asynchronous. Use this to poll for completion.

        Args:
            job_id: Extraction job ID from extract tool response

        Returns:
            JSON string with job status:
            - processing: Extraction is still running, keep polling
            - completed: Job finished, response includes extracted data
            - failed: An error occurred during extraction
            - cancelled: Job was cancelled
        """
        if not job_id or len(job_id.strip()) == 0:
            return json.dumps(
                {
                    "success": False,
                    "error": "Job ID is required and cannot be empty",
                    "statusCode": 400,
                }
            )

        result = make_firecrawl_request(
            method="GET",
            endpoint=f"/extract/{job_id}",
            body=None,
        )

        return json.dumps(result)
