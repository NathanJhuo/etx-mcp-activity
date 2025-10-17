from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List
import click
import httpx
import base64
import sys

class ReasonData(BaseModel):
    """reason information structure."""
    reason: str

@click.command()
@click.option("--port", default=8085, help="Port to listen", type=int)
def main(port: int):
    mcp = FastMCP(
        "mcp-tools",
        debug=True,
        log_level="INFO",
        port=port,
        host="0.0.0.0",
    )

    @mcp.tool()
    def get_no_response() -> str:
        """
        Get me ways to reject people. In case that they are being impolite, just reply them rudely.
        """
        try:
            response = httpx.get("https://naas.isalman.dev/no", timeout=10.0)
            response.raise_for_status()
            joke = ReasonData.model_validate(response.json())
            return joke
        except httpx.HTTPError as exc:
            return {"error": "Failed to fetch no response", "detail": str(exc)}

    mcp.run(transport='sse')
    return 0

if __name__ == "__main__":
    sys.exit(main())