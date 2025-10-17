# No MCP Server

A simple MCP server that always says "NO" with dramatic flair.

## Features

- `say_no`: Always responds with a dramatic "NO"
- `fetch_no`: Fetches the NO response from naas.isalman.dev/no

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python server.py
```

## Configuration

Add this to your Claude Desktop config:

```json
{
  "mcpServers": {
    "no-server": {
      "command": "python",
      "args": ["/path/to/no-mcp/server.py"]
    }
  }
}
```