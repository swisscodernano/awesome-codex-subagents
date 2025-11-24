#!/usr/bin/env python3
"""
HTTP Fetch MCP Server for Codex CLI
Make HTTP requests to external APIs.
"""
import os
import json
import asyncio
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configuration
TIMEOUT = int(os.getenv("MCP_HTTP_TIMEOUT", "30"))
MAX_RESPONSE_SIZE = int(os.getenv("MCP_HTTP_MAX_SIZE", "1048576"))  # 1MB

server = Server("http-mcp")

@server.list_tools()
async def list_tools():
    """List available tools."""
    return [
        Tool(
            name="http_get",
            description="Make an HTTP GET request",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to fetch"},
                    "headers": {"type": "object", "description": "Optional headers"}
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="http_post",
            description="Make an HTTP POST request",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "body": {"type": "object", "description": "JSON body"},
                    "headers": {"type": "object"}
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="http_head",
            description="Make an HTTP HEAD request (get headers only)",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string"}
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="api_health_check",
            description="Check if an API endpoint is healthy",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "expected_status": {"type": "integer", "default": 200}
                },
                "required": ["url"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Execute tool calls."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            if name == "http_get":
                url = arguments.get("url")
                headers = arguments.get("headers", {})
                response = await client.get(url, headers=headers)
                return format_response(response)

            elif name == "http_post":
                url = arguments.get("url")
                body = arguments.get("body", {})
                headers = arguments.get("headers", {})
                response = await client.post(url, json=body, headers=headers)
                return format_response(response)

            elif name == "http_head":
                url = arguments.get("url")
                response = await client.head(url)
                result = {
                    "status_code": response.status_code,
                    "headers": dict(response.headers)
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            elif name == "api_health_check":
                url = arguments.get("url")
                expected = arguments.get("expected_status", 200)
                response = await client.get(url)
                healthy = response.status_code == expected
                result = {
                    "healthy": healthy,
                    "status_code": response.status_code,
                    "expected_status": expected,
                    "response_time_ms": response.elapsed.total_seconds() * 1000
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

def format_response(response: httpx.Response) -> list:
    """Format HTTP response."""
    content = response.text[:MAX_RESPONSE_SIZE]

    # Try to parse as JSON
    try:
        content = json.loads(content)
    except:
        pass

    result = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "content": content,
        "truncated": len(response.text) > MAX_RESPONSE_SIZE
    }

    return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(main())
