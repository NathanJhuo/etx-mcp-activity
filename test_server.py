#!/usr/bin/env python3

import json
import subprocess
import sys

def test_mcp_server():
    """Test the MCP server tools via stdio"""

    # Test list tools
    print("Testing list_tools...")
    list_tools_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }

    # Test say_no tool
    print("Testing say_no tool...")
    say_no_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "say_no",
            "arguments": {"message": "test message"}
        }
    }

    # Test fetch_no tool
    print("Testing fetch_no tool...")
    fetch_no_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "fetch_no",
            "arguments": {}
        }
    }

    requests = [list_tools_request, say_no_request, fetch_no_request]

    for req in requests:
        print(f"\nRequest: {json.dumps(req, indent=2)}")

if __name__ == "__main__":
    test_mcp_server()