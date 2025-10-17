#!/usr/bin/env python3

import httpx
import logging
from typing import Optional
from pydantic import BaseModel
import click
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("no-mcp-server")

class NoData(BaseModel):
    """Data model for NO response"""
    url: str
    status_code: int
    response: str
    headers: dict
    timestamp: Optional[str] = None

# Create FastMCP server
mcp = FastMCP("No MCP Server")

@mcp.tool()
def say_no(message: str = "") -> str:
    """Always responds with a dramatic 'NO'

    Args:
        message: Any message you want to reject (optional)

    Returns:
        A dramatic NO response
    """
    logger.info(f"Saying NO to: {message}")
    return "🎭 Insert an orchestra sound: dun dun dun NO."

@mcp.tool()
def fetch_no() -> str:
    """Fetches the NO response from naas.isalman.dev/no and returns it as JSON

    Returns:
        JSON formatted response from the NO endpoint
    """
    try:
        logger.info("Fetching from naas.isalman.dev/no")

        with httpx.Client() as client:
            response = client.get("https://naas.isalman.dev/no")
            response.raise_for_status()

            no_data = NoData(
                url="https://naas.isalman.dev/no",
                status_code=response.status_code,
                response=response.text,
                headers=dict(response.headers)
            )

            logger.info("Successfully fetched NO response")
            return no_data.model_dump_json(indent=2)

    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching NO: {e}")
        error_data = {
            "url": "https://naas.isalman.dev/no",
            "error": str(e),
            "status": "failed"
        }
        return str(error_data)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        error_data = {
            "url": "https://naas.isalman.dev/no",
            "error": str(e),
            "status": "failed"
        }
        return str(error_data)

@click.command()
def main():
    """Run the No MCP Server"""
    logger.info("Starting No MCP Server")
    mcp.run()

if __name__ == "__main__":
    main()