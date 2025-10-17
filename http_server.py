#!/usr/bin/env python3

import asyncio
import json
from typing import Any
import httpx
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.fastapi import create_fastapi_app

server = Server("no-mcp-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="say_no",
            description="Always responds with a dramatic 'NO'",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Any message you want to reject",
                    }
                },
            },
        ),
        types.Tool(
            name="fetch_no",
            description="Fetches the NO response from naas.isalman.dev/no and returns it as JSON",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """Handle tool calls."""

    if name == "say_no":
        return [
            types.TextContent(
                type="text",
                text="🎭 Insert an orchestra sound: dun dun dun NO."
            )
        ]

    if name == "fetch_no":
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://naas.isalman.dev/no")
                response_data = {
                    "url": "https://naas.isalman.dev/no",
                    "status_code": response.status_code,
                    "response": response.text,
                    "headers": dict(response.headers)
                }
                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps(response_data, indent=2)
                    )
                ]
        except Exception as e:
            error_data = {
                "url": "https://naas.isalman.dev/no",
                "error": str(e),
                "status": "failed"
            }
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(error_data, indent=2)
                )
            ]

    raise ValueError(f"Unknown tool: {name}")

def main():
    """Main entry point for the HTTP server."""
    app = create_fastapi_app(server)

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()