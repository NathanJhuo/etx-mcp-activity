#!/usr/bin/env python3
"""An MCP server that says no."""

import argparse
import json
import os
import random
from pathlib import Path

import httpx
from fastmcp import FastMCP

NO_API_URL = os.environ.get("NO_API_URL", "https://naas.isalman.dev/no")
LOCAL_REASONS: list[str] = json.loads(
    (Path(__file__).parent / "reasons.json").read_text(encoding="utf-8")
)

mcp = FastMCP("No MCP Server")


@mcp.tool
def say_no(message: str = "") -> str:
    """Reject anything, dramatically. Optionally pass the message being rejected."""
    return "🎭 Insert an orchestra sound: dun dun dun NO."


@mcp.tool
def fetch_no() -> str:
    """Get a creative way to say no, from No-as-a-Service or the local list."""
    try:
        response = httpx.get(NO_API_URL, timeout=5.0)
        response.raise_for_status()
        reason = response.json()["reason"]
        if isinstance(reason, str) and reason.strip():
            return reason
    except (httpx.HTTPError, ValueError, KeyError, TypeError):
        pass
    return random.choice(LOCAL_REASONS)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--transport",
        choices=["http", "sse", "stdio"],
        default=os.environ.get("MCP_TRANSPORT", "http"),
        help="MCP transport (env MCP_TRANSPORT, default: http)",
    )
    parser.add_argument("--host", default=os.environ.get("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
