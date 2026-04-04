"""CLI argument parser for Firecrawl MCP Server."""

import argparse


def parse_args():
    """Parse command-line arguments for transport, host, and port."""
    parser = argparse.ArgumentParser(description="Firecrawl MCP Server")
    parser.add_argument(
        "-t",
        "--transport",
        help="Transport method for MCP (Allowed Values: 'stdio', or 'streamable-http')",
        default="streamable-http",
    )
    parser.add_argument("--host", help="Host to bind the server to", default=None)
    parser.add_argument(
        "--port", type=int, help="Port to bind the server to", default=None
    )
    return parser.parse_args()
