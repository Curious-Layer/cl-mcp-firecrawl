"""Configuration and logging setup for Firecrawl MCP Server."""

import logging

# Firecrawl API configuration
FIRECRAWL_API_BASE = "https://api.firecrawl.dev"
FIRECRAWL_API_VERSION = "v2"

# Default API timeout (seconds)
API_TIMEOUT = 30


def configure_logging() -> None:
    """Configure logging for the Firecrawl MCP Server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
