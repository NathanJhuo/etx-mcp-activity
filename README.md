# No MCP Server

An [MCP](https://modelcontextprotocol.io) server that says no.

Tools:

- `say_no(message="")`: always answers with a dramatic "NO".
- `fetch_no()`: returns a creative rejection from
  [No-as-a-Service](https://naas.isalman.dev/no). If that service is unreachable
  or returns something unexpected, it answers from a bundled list of 1000+ reasons
  in `reasons.json`.

## Configuration

| Setting      | CLI flag      | Env var         | Default                         |
| ------------ | ------------- | --------------- | ------------------------------- |
| Transport    | `--transport` | `MCP_TRANSPORT` | `http` (`http`, `sse`, `stdio`) |
| Bind host    | `--host`      | `HOST`          | `0.0.0.0`                       |
| Bind port    | `--port`      | `PORT`          | `8000`                          |
| Upstream URL | -             | `NO_API_URL`    | `https://naas.isalman.dev/no`   |

With the `http` transport the MCP endpoint is `http://<host>:<port>/mcp`.

## Run locally

Requires Python 3.10+.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python server.py                      # HTTP on 0.0.0.0:8000
.venv/bin/python server.py --transport stdio    # stdio
```

## Run in a container

The image is based on `registry.access.redhat.com/ubi9/python-312` and runs as user 1001.

```bash
podman build -t no-mcp .
podman run -d --name no-mcp -p 8000:8000 no-mcp
```

`docker` works the same way.

## MCP client configuration

HTTP (server already running, locally or in a container):

```json
{
  "mcpServers": {
    "no-server": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Claude Code: `claude mcp add --transport http no-server http://localhost:8000/mcp`

stdio (for example, Claude Desktop launching the server itself):

```json
{
  "mcpServers": {
    "no-server": {
      "command": "/path/to/.venv/bin/python",
      "args": ["/path/to/server.py", "--transport", "stdio"]
    }
  }
}
```

## Attribution

Most entries in `reasons.json` come from
[hotheadhacker/no-as-a-service](https://github.com/hotheadhacker/no-as-a-service)
(deduplicated, with additional entries added to this project), used under the
MIT License:

```
MIT License

Copyright (c) 2026 hotheadhacker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
