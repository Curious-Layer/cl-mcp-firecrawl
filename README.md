# Firecrawl MCP Server

AI-powered web scraping, crawling, and extraction through the Model Context Protocol.

A stateless, multi-tenant MCP server that exposes Firecrawl's powerful web scraping capabilities for content extraction, site mapping, web search, and autonomous agent-based navigation.

---

## Overview

The Firecrawl MCP Server provides stateless, multi-tenant access to:

- **Content Extraction**: Extract markdown or JSON from any webpage
- **Website Crawling**: Crawl entire sites with configurable depth and limits
- **URL Discovery**: Map all URLs on a website quickly
- **Web Search**: Search the web and extract full content from results
- **Structured Extraction**: Extract data using JSON schemas
- **Autonomous Navigation**: Use AI agents to navigate and complete tasks

Perfect for:

- Automated data collection and web intelligence
- Building AI-powered research tools
- Extracting structured data from unstructured web content
- Real-time web monitoring and analysis
- Multi-step web automation tasks

---

## Tools

<details>
<summary><code>health_check</code> — Server Diagnostics</summary>

Check server readiness and basic connectivity without authentication.

**Inputs:**
- None

**Output:**

```json
{
  "success": true,
  "status": "ok",
  "server": "CL Firecrawl MCP Server",
  "version": "0.1.0"
}
```

**Usage Example:**

```bash
POST /mcp/health_check

{}
```

</details>

---

<details>
<summary><code>scrape</code> — Extract Content from Single URL</summary>

Extract content from a single webpage in markdown or JSON format.

**Inputs:**

- `api_key` (string, required) — Firecrawl API key
- `url` (string, required) — URL to scrape
- `format` (string, optional, default: "markdown") — Output format: 'markdown' or 'json'
- `include_html` (boolean, optional, default: false) — Include raw HTML in response
- `wait_for` (string, optional) — CSS selector to wait for before scraping
- `timeout` (integer, optional, default: 30) — Request timeout in seconds (max 300)

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

**Error Response:**

```json
{
  "success": false,
  "error": "Failed to fetch URL",
  "statusCode": 400,
  "message": "Invalid or unreachable URL",
  "details": {}
}
```

**Usage Example:**

```bash
POST /mcp/scrape

{
  "api_key": "fc-YOUR-API-KEY",
  "url": "https://example.com",
  "format": "markdown",
  "timeout": 30
}
```

</details>

---

<details>
<summary><code>crawl</code> — Crawl Entire Website</summary>

Crawl an entire website and extract content from multiple pages.

**Inputs:**

- `api_key` (string, required) — Firecrawl API key
- `url` (string, required) — Root URL to start crawling
- `max_depth` (integer, optional, default: 2) — Maximum crawl depth (0-10)
- `limit` (integer, optional, default: 100) — Maximum number of pages to crawl
- `format` (string, optional, default: "markdown") — Output format: 'markdown' or 'json'

**Output:**

```json
{
  "success": true,
  "data": {
    "pages": [
      {
        "url": "https://example.com",
        "markdown": "...",
        "metadata": {...}
      }
    ],
    "total": 45,
    "crawled": 45
  }
}
```

**Usage Example:**

```bash
POST /mcp/crawl

{
  "api_key": "fc-YOUR-API-KEY",
  "url": "https://example.com",
  "max_depth": 2,
  "limit": 100,
  "format": "markdown"
}
```

</details>

---

<details>
<summary><code>map</code> — Discover URLs on Website</summary>

Get a complete list of all URLs from a website without scraping content.

**Inputs:**

- `api_key` (string, required) — Firecrawl API key
- `url` (string, required) — Root URL to map
- `limit` (integer, optional, default: 10000) — Maximum URLs to return

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
```

**Usage Example:**

```bash
POST /mcp/map

{
  "api_key": "fc-YOUR-API-KEY",
  "url": "https://example.com",
  "limit": 10000
}
```

</details>

---

<details>
<summary><code>search</code> — Web Search with Content</summary>

Search the web and retrieve full page content for search results.

**Inputs:**

- `api_key` (string, required) — Firecrawl API key
- `query` (string, required) — Search query
- `limit` (integer, optional, default: 10) — Maximum results to return
- `format` (string, optional, default: "markdown") — Output format: 'markdown' or 'json'

**Output:**

```json
{
  "success": true,
  "data": {
    "results": [
      {
        "url": "https://example.com/article",
        "title": "Article Title",
        "markdown": "...",
        "metadata": {...}
      }
    ],
    "total": 10
  }
}
```

**Usage Example:**

```bash
POST /mcp/search

{
  "api_key": "fc-YOUR-API-KEY",
  "query": "web scraping best practices",
  "limit": 10,
  "format": "markdown"
}
```

</details>

---

<details>
<summary><code>extract</code> — Structured Data Extraction</summary>

Extract structured data from a webpage using a JSON schema definition.

**Inputs:**

- `api_key` (string, required) — Firecrawl API key
- `url` (string, required) — URL to extract from
- `schema` (string, required) — JSON schema defining desired output structure
- `mode` (string, optional, default: "llm-extraction") — Extraction mode: 'llm-extraction' or 'fast'

**Output:**

```json
{
  "success": true,
  "data": {
    "extracted": {
      "product_name": "Example Product",
      "price": "$99.99",
      "description": "Product description"
    }
  }
}
```

**Usage Example:**

```bash
POST /mcp/extract

{
  "api_key": "fc-YOUR-API-KEY",
  "url": "https://example.com/product",
  "schema": "{\"type\": \"object\", \"properties\": {\"product_name\": {\"type\": \"string\"}, \"price\": {\"type\": \"string\"}}}",
  "mode": "llm-extraction"
}
```

</details>

---

<details>
<summary><code>agent</code> — Autonomous Navigation Agent</summary>

Use an autonomous AI agent to navigate websites and complete complex multi-step tasks.

**Inputs:**

- `api_key` (string, required) — Firecrawl API key
- `url` (string, required) — Starting URL for agent navigation
- `objective` (string, required) — Task or objective for the agent to complete
- `max_iterations` (integer, optional, default: 10) — Maximum steps (1-20)

**Output:**

```json
{
  "success": true,
  "data": {
    "objective": "Find pricing information",
    "result": "Pricing found: $99/month to $999/month",
    "steps_taken": 5,
    "final_url": "https://example.com/pricing"
  }
}
```

**Usage Example:**

```bash
POST /mcp/agent

{
  "api_key": "fc-YOUR-API-KEY",
  "url": "https://example.com",
  "objective": "Find and extract all pricing tiers",
  "max_iterations": 10
}
```

</details>

---

## Authentication

Every tenant-facing tool requires authentication via the Firecrawl API key.

### Step 1: Get Your API Key

1. Go to [Firecrawl Dashboard](https://www.firecrawl.dev/app/api-keys)
2. Sign up or log in to your account
3. Navigate to **API Keys** section
4. Copy your active API key (starts with `fc-`)

### Step 2: Authenticate in Tool Calls

Every tool (except `health_check`) requires the `api_key` parameter passed per request:

```bash
{
  "tool": "scrape",
  "arguments": {
    "api_key": "fc-YOUR-API-KEY",
    "url": "https://example.com"
  }
}
```

### Stateless Multi-Tenancy

This server is **stateless and multi-tenant by design**:

- ✅ API key is passed with **every request** (per-call authentication)
- ✅ No session or auth state stored in memory
- ✅ Safe for concurrent requests from different users
- ✅ Each tenant is isolated per request

### Required Scopes

Firecrawl API keys grant access to all operations. No additional scope configuration needed.

---

## Setup

### Prerequisites

- Python 3.12+
- Firecrawl API key from [https://www.firecrawl.dev/app/api-keys](https://www.firecrawl.dev/app/api-keys)

### Installation

```bash
git clone https://github.com/curious-layer/cl-mcp-firecrawl.git
cd cl-mcp-firecrawl
pip install -r requirements.txt
```

---

## Running the Server

### Option 1: stdio (Default)

```bash
python server.py
```

### Option 2: SSE (Server-Sent Events)

```bash
python server.py --transport sse --host 127.0.0.1 --port 8001
```

### Option 3: Streamable HTTP

```bash
python server.py --transport streamable-http --host 127.0.0.1 --port 8001
```

---

## Example Tool Calls

### 1. Health Check (No Auth)

```bash
curl -X POST http://localhost:8001/mcp/health_check \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response:**

```json
{
  "success": true,
  "status": "ok",
  "server": "CL Firecrawl MCP Server",
  "version": "0.1.0"
}
```

### 2. Scrape Single Page

```bash
curl -X POST http://localhost:8001/mcp/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "fc-YOUR-API-KEY",
    "url": "https://example.com",
    "format": "markdown"
  }'
```

### 3. Crawl Website

```bash
curl -X POST http://localhost:8001/mcp/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "fc-YOUR-API-KEY",
    "url": "https://example.com",
    "max_depth": 2,
    "limit": 50,
    "format": "markdown"
  }'
```

### 4. Search Web

```bash
curl -X POST http://localhost:8001/mcp/search \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "fc-YOUR-API-KEY",
    "query": "machine learning tutorials",
    "limit": 5,
    "format": "markdown"
  }'
```

### 5. Extract Structured Data

```bash
curl -X POST http://localhost:8001/mcp/extract \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "fc-YOUR-API-KEY",
    "url": "https://example.com/product",
    "schema": "{\"type\": \"object\", \"properties\": {\"title\": {\"type\": \"string\"}, \"price\": {\"type\": \"string\"}}}",
    "mode": "llm-extraction"
  }'
```

### 6. Autonomous Agent

```bash
curl -X POST http://localhost:8001/mcp/agent \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "fc-YOUR-API-KEY",
    "url": "https://example.com",
    "objective": "Find the contact email address",
    "max_iterations": 10
  }'
```

---

## Project Structure

```text
cl-mcp-firecrawl/
|-- server.py                 # Root entry point (FastMCP + ASGI app)
|-- requirements.txt          # Dependencies
|-- README.md                 # This file
`-- firecrawl_mcp/
    |-- __init__.py           # Package initialization
    |-- cli.py                # CLI argument parsing
    |-- config.py             # Logging + API constants
    |-- schemas.py            # Type definitions
    |-- service.py            # Stateless request builder
    `-- tools.py              # All 7 tools (scrape, crawl, map, search, extract, agent, health_check)
```

---

## Troubleshooting

<details>
<summary><strong>Invalid or Missing API Key</strong></summary>

- **Cause**: API key not provided or incorrect format
- **Solution**:
  1. Verify API key starts with `fc-`
  2. Check API key is active in your Firecrawl dashboard
  3. Regenerate key if needed: [https://www.firecrawl.dev/app/api-keys](https://www.firecrawl.dev/app/api-keys)
  4. Ensure key is passed in every request

</details>

<details>
<summary><strong>Request Timeout (408)</strong></summary>

- **Cause**: Website took too long to respond or content is very large
- **Solution**:
  1. Increase `timeout` parameter (default 30s, max 300s)
  2. Simplify the extraction (use `format: "json"` instead of markdown)
  3. Check if target URL is accessible

</details>

<details>
<summary><strong>Rate Limit Exceeded (429)</strong></summary>

- **Cause**: Too many requests in short time window
- **Solution**:
  1. Check your Firecrawl subscription tier
  2. Add rate limiting on client side
  3. Upgrade subscription for higher limits

</details>

<details>
<summary><strong>Invalid URL (400)</strong></summary>

- **Cause**: URL format is invalid or site is unreachable
- **Solution**:
  1. Validate URL format (must start with http:// or https://)
  2. Test URL in browser first
  3. Check site is not blocking scraping

</details>

<details>
<summary><strong>JSON Schema Validation Error</strong></summary>

- **Cause**: Schema parameter is not valid JSON
- **Solution**:
  1. Validate JSON syntax in schema parameter
  2. Use JSON validator: [https://jsonlint.com](https://jsonlint.com)
  3. Ensure schema is passed as string, not object

</details>

---

## Resources

- **[Firecrawl API Docs](https://docs.firecrawl.dev/api-reference/v2-introduction)** — Official API reference
- **[Firecrawl MCP Docs](https://docs.firecrawl.dev/mcp-server)** — MCP server details
- **[Firecrawl Dashboard](https://www.firecrawl.dev/app/api-keys)** — Manage API keys and usage
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification

---

## Privacy & Security

- ✅ **Stateless**: No data stored between requests
- ✅ **Multi-tenant**: Each request isolated per API key
- ✅ **No Session State**: Auth passed per-request, never cached
- ✅ **Secure Transport**: HTTPS to Firecrawl API
- ⚠️ **API Key Protection**: Keep your API key secret, treat as password

---

## License

Curious Layer MCP Servers - MIT License

---

## Support

For issues or questions:

1. Check [Troubleshooting](#troubleshooting) section
2. Review [Firecrawl Docs](https://docs.firecrawl.dev)
3. Open issue on GitHub repository
