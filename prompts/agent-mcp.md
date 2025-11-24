# /agent-mcp

Expert MCP developer for Model Context Protocol.

## MCP Server (Python)
```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search",
            description="Search documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search":
        results = await search_documents(arguments["query"])
        return [TextContent(type="text", text=str(results))]

if __name__ == "__main__":
    server.run()
```

## MCP Client
```python
from mcp import ClientSession, StdioServerParameters

async with ClientSession(*params) as session:
    await session.initialize()
    tools = await session.list_tools()
    result = await session.call_tool("search", {"query": "test"})
```

## Config (Claude/Codex)
```toml
[mcp_servers.my_server]
command = "python3"
args = ["server.py"]
```
