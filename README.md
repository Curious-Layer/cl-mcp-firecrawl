**AI-powered web scraping, crawling, and extraction through the Model Context Protocol.**

A Model Context Protocol (MCP) server that exposes Firecrawl's API for intelligent web content extraction, comprehensive website crawling, and structured data mining.

---

## Overview

The Firecrawl MCP Server provides stateless, multi-tenant access to intelligent web intelligence capabilities:

- **Content Extraction**: Scrape and extract markdown, HTML, JSON, and formatted content from single or multiple URLs with flexible filtering
- **Website Crawling**: Crawl entire websites with URL filtering, depth control, and comprehensive scraping options
- **URL Discovery**: Map all URLs on a website with filtering, geographic targeting, and search capabilities
- **Web Search Integration**: Search the web and extract full content from results with advanced geographical and source filtering
- **Structured Data Extraction**: Extract data from URLs using JSON schemas and natural language prompts (asynchronous)
- **Autonomous Agents**: Deploy AI agents to navigate websites and complete complex multi-step tasks (asynchronous)

Perfect for:

- Automated data collection and web intelligence pipelines
- Building AI-powered research and competitive analysis tools
- Extracting structured data from unstructured web content
- Real-time web monitoring and market research
- Multi-step web automation and data enrichment workflows

---

## Tools

<details>
<summary><code>health_check</code> — Server Diagnostics</summary>

Check server readiness and basic connectivity without authentication.

**Inputs:**

```
- None
```

**Output:**

```json
{
  "success": true,
  "status": "ok",
  "server": "CL Firecrawl MCP Server",
  "version": "0.1.0"
}
```

</details>

---

<details>
<summary><code>scrape</code> — Extract Content from Single URL</summary>

Scrape a single URL and extract content in multiple formats with flexible filtering and browser options.

**Inputs:**

```

- `url` (string, required) — The URL to scrape
- `formats` (string, optional, default: "markdown") — Output formats (comma-separated): markdown, html, rawHtml, json, screenshot, links, images, summary, audio, branding, changeTracking
- `only_main_content` (boolean, optional, default: true) — Extract only main content, excluding headers/footers/navs
- `include_tags` (string, optional) — Comma-separated HTML tags to include in output
- `exclude_tags` (string, optional) — Comma-separated HTML tags to exclude from output
- `wait_for_selector` (string, optional) — CSS selector to wait for before scraping
- `timeout_ms` (integer, optional, default: 30000) — Request timeout in milliseconds (1000-300000)
- `mobile` (boolean, optional, default: false) — Emulate mobile device (responsive layout)
- `skip_tls_verification` (boolean, optional, default: true) — Skip TLS certificate verification
- `proxy` (string, optional, default: "auto") — Proxy type: basic, enhanced, or auto
- `block_ads` (boolean, optional, default: true) — Block ads and cookie popups
- `remove_base64_images` (boolean, optional, default: true) — Remove base64 encoded images from markdown

```

**Output:**

```json
{
  "success": true,
  "data": {
    "markdown": "# Page Title\n\nPage content...",
    "html": "<html>...</html>",
    "metadata": {
      "title": "Page Title",
      "description": "Page description",
      "url": "https://example.com"
    }
  }
}
```

</details>

---

<details>
<summary><code>crawl</code> — Crawl Entire Website</summary>

Crawl an entire website with URL filtering, discovery depth control, and comprehensive scraping options for each page.
**Inputs:**

```
- `url` (string, required) — The base URL to start crawling from
- `prompt` (string, optional) — Natural language prompt to generate crawler options
- `exclude_paths` (string, optional) — Comma-separated regex patterns for URLs to exclude
- `include_paths` (string, optional) — Comma-separated regex patterns for URLs to include
- `max_discovery_depth` (integer, optional) — Maximum depth based on discovery order
- `sitemap` (string, optional, default: "include") — Sitemap mode: skip, include, or only
- `ignore_query_parameters` (boolean, optional, default: false) — Don't re-scrape same path with different query parameters
- `regex_on_full_url` (boolean, optional, default: false) — Match patterns against full URL including query parameters
- `limit` (integer, optional, default: 10000) — Maximum number of pages to crawl
- `crawl_entire_domain` (boolean, optional, default: false) — Follow sibling and parent URLs, not just child paths
- `allow_external_links` (boolean, optional, default: false) — Allow crawler to follow external links
- `allow_subdomains` (boolean, optional, default: false) — Allow crawler to follow subdomains
- `delay` (float, optional) — Delay in seconds between scrapes
- `max_concurrency` (integer, optional) — Maximum concurrent scrapes
- `formats` (string, optional, default: "markdown") — Output formats (comma-separated)
- `only_main_content` (boolean, optional, default: true) — Extract only main content, excluding headers/footers
- `include_tags` (string, optional) — Comma-separated HTML tags to include
- `exclude_tags` (string, optional) — Comma-separated HTML tags to exclude
- `wait_for_selector` (string, optional) — CSS selector to wait for before scraping
- `mobile` (boolean, optional, default: false) — Emulate mobile device
- `skip_tls_verification` (boolean, optional, default: true) — Skip TLS certificate verification
- `proxy` (string, optional, default: "auto") — Proxy type: basic, enhanced, or auto
- `block_ads` (boolean, optional, default: true) — Block ads and cookie popups
- `remove_base64_images` (boolean, optional, default: true) — Remove base64 encoded images
- `zero_data_retention` (boolean, optional, default: false) — Enable zero data retention
```

**Output:**

```json
{
  "success": true,
  "id": "crawl-job-id",
  "data": {
    "pages": [...],
    "total": 45,
    "crawled": 45
  }
}
```

</details>

---

<details>
<summary><code>map</code> — Map and Discover URLs on Website</summary>

Get a complete list of all URLs from a website with optional filtering, search, and geographic targeting.

**Inputs:**

````
- `url` (string, required) — The base URL to start mapping from
- `search` (string, optional) — Search query to filter and order results by relevance
- `sitemap` (string, optional, default: "include") — Sitemap mode: skip, include, or only
- `include_subdomains` (boolean, optional, default: true) — Include subdomains of the website
- `ignore_query_parameters` (boolean, optional, default: true) — Don't return URLs with query parameters
- `ignore_cache` (boolean, optional, default: false) — Bypass sitemap cache to get fresh URLs
- `limit` (integer, optional, default: 5000) — Maximum number of URLs to return (max 100000)
- `timeout_ms` (integer, optional) — Timeout in milliseconds
- `country` (string, optional) — ISO 3166-1 alpha-2 country code (e.g., US, DE, JP)
- `languages` (string, optional) — Comma-separated preferred languages (e.g., en-US,de-DE)
```

**Output:**

```json
{
  "success": true,
  "data": {
    "urls": [
      "https://example.com",
      "https://example.com/about",
      "https://example.com/products"
    ],
    "total": 150
  }
}
````

</details>

---

<details>
<summary><code>search</code> — Web Search with Content Extraction</summary>

Search the web and retrieve content from results with advanced geographical and source filtering options.

**Inputs:**

```
- `query` (string, required, max 500 characters) — Search query
- `limit` (integer, optional, default: 5, range: 1-100) — Maximum number of results to return
- `sources` (string, optional, default: "web") — Search sources (comma-separated): web, images, news
- `categories` (string, optional) — Filter by categories (comma-separated): github, research, pdf
- `tbs` (string, optional) — Time-based search filter (e.g., qdr:d for past day, qdr:w for past week, qdr:m for past month)
- `location` (string, optional) — Geographic location for search results (e.g., San Francisco,California,United States)
- `country` (string, optional) — ISO country code for geo-targeting (e.g., US, DE, FR, JP)
- `timeout` (integer, optional, default: 60000) — Timeout in milliseconds (range: 1000-300000)
- `ignore_invalid_urls` (boolean, optional, default: false) — Exclude invalid URLs from search results
- `enterprise` (string, optional) — Enterprise search options (comma-separated): anon, zdr (Zero Data Retention)
- `formats` (string, optional, default: "markdown") — Scrape output formats (comma-separated)
- `mobile` (boolean, optional, default: false) — Emulate mobile device when scraping results
- `proxy` (string, optional, default: "auto") — Proxy type: basic, enhanced, or auto
- `block_ads` (boolean, optional, default: true) — Enable ad-blocking and cookie popup blocking
```

**Output:**

```json
{
  "success": true,
  "data": {
    "web": [
      {
        "url": "https://example.com/article",
        "title": "Article Title",
        "description": "Description..."
      }
    ]
  },
  "creditsUsed": 5
}
```

</details>

---

<details>
<summary><code>extract</code> — Async Structured Data Extraction</summary>

Start an asynchronous extraction job to extract structured data from URLs using LLMs and JSON schemas.

**Inputs:**

```
- `urls` (string, required) — Comma-separated URLs to extract data from (glob format supported)
- `prompt` (string, optional) — Custom prompt to guide the extraction process
- `schema` (string, optional) — JSON schema to structure the extracted data
- `enable_web_search` (boolean, optional, default: false) — Use web search to find additional data during extraction
- `ignore_sitemap` (boolean, optional, default: false) — Ignore sitemap.xml files during website scanning
- `include_subdomains` (boolean, optional, default: true) — Include subdomains when scanning URLs
- `show_sources` (boolean, optional, default: false) — Include sources used for extraction in response
- `ignore_invalid_urls` (boolean, optional, default: true) — Ignore invalid URLs instead of failing entire request
- `formats` (string, optional, default: "markdown") — Scrape output formats (comma-separated)
- `only_main_content` (boolean, optional, default: true) — Extract only main content, excluding headers/footers
- `mobile` (boolean, optional, default: false) — Emulate mobile device during scraping
- `proxy` (string, optional, default: "auto") — Proxy type: basic, enhanced, or auto
- `block_ads` (boolean, optional, default: true) — Enable ad-blocking and cookie popup blocking
```

**Output:**

```json
{
  "success": true,
  "id": "extraction-job-uuid"
}
```

</details>

---

<details>
<summary><code>extract_status</code> — Check Extraction Job Status</summary>

Check the status of an extraction job and retrieve results when complete.

**Inputs:**

```
- `job_id` (string, required) — The extraction job ID returned by the extract tool (UUID format)
```

**Output:**

```json
{
  "success": true,
  "status": "completed",
  "data": {
    "extracted_data": [...]
  },
  "tokensUsed": 1250
}
```

</details>

---

<details>
<summary><code>agent</code> — Autonomous Navigation Agent (Async)</summary>

Start an asynchronous autonomous AI agent to navigate websites and complete complex multi-step tasks.

**Inputs:**

```
- `prompt` (string, required, max 10000 characters) — Natural language description of data to extract or task to complete
- `urls` (string, optional) — Comma-separated URLs to constrain the agent to
- `schema` (string, optional) — JSON schema for structured output
- `model` (string, optional, default: "spark-1-mini") — Model to use: spark-1-mini (cheaper, 60% less) or spark-1-pro (higher accuracy)
- `strict_constrain_to_urls` (boolean, optional, default: false) — If true, agent will only visit URLs provided in urls parameter
- `max_credits` (float, optional, default: 2500) — Maximum credits to spend on this agent task
```

**Output:**

```json
{
  "success": true,
  "id": "agent-job-uuid"
}
```

</details>

---

<details>
<summary><code>agent_status</code> — Check Agent Job Status</summary>

Check the status of an agent job and retrieve results when complete. Poll every 15-30 seconds.

**Inputs:**

```
- `job_id` (string, required) — The agent job ID returned by the agent tool (UUID format)
```

**Output:**

```json
{
  "success": true,
  "status": "completed",
  "data": {
    "extracted_data": {...}
  },
  "model": "spark-1-mini",
  "creditsUsed": 150
}
```

</details>

---

<details>
<summary><strong>Common Parameters</strong></summary>

These parameters are shared across multiple tools:

- `url` — The target URL to scrape, crawl, or map
- `urls` — Comma-separated list of target URLs (for extraction/search)
- `formats` — Output format types (comma-separated): markdown, html, rawHtml, json, screenshot, links, images, summary, audio, branding, changeTracking
- `timeout` or `timeout_ms` — Request timeout in milliseconds (range: 1000-300000ms)
- `mobile` — Emulate mobile device for responsive layouts (default: false)
- `proxy` — Proxy strategy: basic, enhanced, or auto (default: auto)
- `block_ads` — Block ads and cookie popups (default: true)
- `only_main_content` — Extract only main content, excluding headers/footers/navigation (default: true)

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Job IDs:**

```
UUID format (e.g., "550e8400-e29b-41d4-a716-446655440000")
```

**URL Patterns:**

```
Single: https://example.com
Multiple (comma-separated): https://example.com/page1,https://example.com/page2
Glob patterns: https://example.com/products/*.html
```

**Status Values:**

```
health_check: success (true/false)
Scrape/Crawl/Map/Search: success (true/false)
Async jobs (agent, extract): processing, completed, failed, cancelled
```

**Output Formats:**

```
markdown, html, rawHtml, json, screenshot, links, images, summary, audio, branding, changeTracking
```

**Search Sources:**

```
web, images, news
```

</details>

---

## Getting Your Firecrawl API Key

1. Go to [Firecrawl Dashboard](https://www.firecrawl.dev/app/api-keys)
2. Sign up or log in to your account
3. Navigate to **API Keys** section
4. Click **Create API Key** or copy your existing active key (starts with `fc-`)
5. Copy the generated key — **you will only see it once**

---

## Troubleshooting

<details>
<summary><strong>Missing or Invalid Firecrawl API Key</strong></summary>

- **Cause:** API key not provided in request parameters or incorrect format
- **Solution:**
  1. Verify API key starts with `fc-`
  2. Check API key is active in your Firecrawl dashboard
  3. Regenerate API key if expired: [Firecrawl Dashboard](https://www.firecrawl.dev/app/api-keys)
  4. Ensure key is passed in every tool request

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No {SERVICE_NAME} credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCp dashboard
  2. Connect your {SERVICE_NAME} account (OAuth) or add your API key (static)
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Rate Limit Exceeded (429)</strong></summary>

- **Cause:** Too many requests in short time window, exceeding API rate limits
- **Solution:**
  1. Check your Firecrawl subscription tier and current usage
  2. Add request throttling on your client side
  3. Upgrade your Firecrawl subscription for higher rate limits

</details>

<details>
<summary><strong>Request Timeout</strong></summary>

- **Cause:** Website took too long to respond or content is very large
- **Solution:**
  1. Increase `timeout_ms` parameter (default 30000ms, max 300000ms)
  2. Check if target URL is accessible and responding normally
  3. Try with simpler extraction parameters first (e.g., markdown only)

</details>

<details>
<summary><strong>Invalid URL Format (400)</strong></summary>

- **Cause:** URL format is invalid or site is unreachable/blocking automated scraping
- **Solution:**
  1. Validate URL format (must start with `http://` or `https://`)
  2. Test URL in browser first to confirm accessibility
  3. Check if site is blocking automated scraping (may require proxy option)
  4. Verify URL is not behind authentication/paywall

</details>

<details>
<summary><strong>Job Status Not Found</strong></summary>

- **Cause:** Job ID is invalid, expired, or does not exist
- **Solution:**
  1. Verify job ID format is correct UUID
  2. Check that you're polling within the expiration window (typically 24-48 hours)
  3. Confirm job ID was returned by initial extraction/agent request
  4. Create a new job if the original has expired

</details>

<details>
<summary><strong>JSON Schema Validation Error</strong></summary>

- **Cause:** Schema parameter is not valid JSON or doesn't follow JSON Schema standard
- **Solution:**
  1. Validate JSON syntax in schema parameter using [jsonlint.com](https://jsonlint.com)
  2. Ensure schema is passed as string, not object literal
  3. Review JSON Schema specification for correct syntax
  4. Test schema against sample data before using

</details>

<details>
<summary><strong>Firecrawl API Error</strong></summary>

- **Cause:** Upstream Firecrawl API returned an error (429, 500, timeout, etc.)
- **Solution:**
  1. Check [Firecrawl Status Page](https://status.firecrawl.dev) for service incidents
  2. Review error message for specific details from Firecrawl API
  3. Verify your API key has sufficient credits
  4. Contact Firecrawl support if problem persists

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Firecrawl API Documentation](https://docs.firecrawl.dev/api-reference/v2-introduction)** — Official API reference and endpoint documentation
- **[Firecrawl Dashboard](https://www.firecrawl.dev/app/api-keys)** — Manage API keys, credits, and subscription
- **[Firecrawl Status Page](https://status.firecrawl.dev)** — Service status and incident reports
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP framework specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
