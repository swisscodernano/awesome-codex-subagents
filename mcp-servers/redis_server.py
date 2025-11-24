#!/usr/bin/env python3
"""
Redis MCP Server for Codex CLI
Cache, pub/sub, and key-value operations.
"""
import os
import json
import asyncio
import redis
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
MAX_KEYS = int(os.getenv("MCP_REDIS_MAX_KEYS", "100"))
READONLY = os.getenv("MCP_REDIS_READONLY", "false").lower() == "true"

server = Server("redis-mcp")

def get_client():
    """Get Redis client."""
    return redis.from_url(REDIS_URL, decode_responses=True)

@server.list_tools()
async def list_tools():
    """List available tools."""
    tools = [
        Tool(
            name="redis_get",
            description="Get a value by key",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Redis key"}
                },
                "required": ["key"]
            }
        ),
        Tool(
            name="redis_keys",
            description="List keys matching a pattern",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Pattern (e.g., 'user:*')", "default": "*"}
                }
            }
        ),
        Tool(
            name="redis_type",
            description="Get the type of a key",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"}
                },
                "required": ["key"]
            }
        ),
        Tool(
            name="redis_ttl",
            description="Get TTL of a key in seconds",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"}
                },
                "required": ["key"]
            }
        ),
        Tool(
            name="redis_info",
            description="Get Redis server info",
            inputSchema={
                "type": "object",
                "properties": {
                    "section": {"type": "string", "description": "Info section (server, memory, stats, etc.)"}
                }
            }
        ),
        Tool(
            name="redis_hgetall",
            description="Get all fields of a hash",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"}
                },
                "required": ["key"]
            }
        ),
        Tool(
            name="redis_lrange",
            description="Get elements from a list",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "start": {"type": "integer", "default": 0},
                    "end": {"type": "integer", "default": -1}
                },
                "required": ["key"]
            }
        ),
        Tool(
            name="redis_smembers",
            description="Get all members of a set",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {"type": "string"}
                },
                "required": ["key"]
            }
        )
    ]

    if not READONLY:
        tools.extend([
            Tool(
                name="redis_set",
                description="Set a key-value pair",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "key": {"type": "string"},
                        "value": {"type": "string"},
                        "ex": {"type": "integer", "description": "Expiry in seconds"}
                    },
                    "required": ["key", "value"]
                }
            ),
            Tool(
                name="redis_del",
                description="Delete a key",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "key": {"type": "string"}
                    },
                    "required": ["key"]
                }
            ),
            Tool(
                name="redis_expire",
                description="Set expiry on a key",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "key": {"type": "string"},
                        "seconds": {"type": "integer"}
                    },
                    "required": ["key", "seconds"]
                }
            )
        ])

    return tools

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Execute tool calls."""
    try:
        client = get_client()

        if name == "redis_get":
            key = arguments.get("key")
            value = client.get(key)
            return [TextContent(type="text", text=json.dumps({"key": key, "value": value}, indent=2))]

        elif name == "redis_keys":
            pattern = arguments.get("pattern", "*")
            keys = client.keys(pattern)[:MAX_KEYS]
            return [TextContent(type="text", text=json.dumps({
                "pattern": pattern,
                "keys": keys,
                "count": len(keys),
                "truncated": len(keys) >= MAX_KEYS
            }, indent=2))]

        elif name == "redis_type":
            key = arguments.get("key")
            key_type = client.type(key)
            return [TextContent(type="text", text=json.dumps({"key": key, "type": key_type}, indent=2))]

        elif name == "redis_ttl":
            key = arguments.get("key")
            ttl = client.ttl(key)
            return [TextContent(type="text", text=json.dumps({"key": key, "ttl": ttl}, indent=2))]

        elif name == "redis_info":
            section = arguments.get("section")
            info = client.info(section) if section else client.info()
            return [TextContent(type="text", text=json.dumps(info, indent=2, default=str))]

        elif name == "redis_hgetall":
            key = arguments.get("key")
            data = client.hgetall(key)
            return [TextContent(type="text", text=json.dumps({"key": key, "data": data}, indent=2))]

        elif name == "redis_lrange":
            key = arguments.get("key")
            start = arguments.get("start", 0)
            end = arguments.get("end", -1)
            items = client.lrange(key, start, end)
            return [TextContent(type="text", text=json.dumps({"key": key, "items": items}, indent=2))]

        elif name == "redis_smembers":
            key = arguments.get("key")
            members = list(client.smembers(key))
            return [TextContent(type="text", text=json.dumps({"key": key, "members": members}, indent=2))]

        elif name == "redis_set" and not READONLY:
            key = arguments.get("key")
            value = arguments.get("value")
            ex = arguments.get("ex")
            client.set(key, value, ex=ex)
            return [TextContent(type="text", text=f"OK: Set {key}")]

        elif name == "redis_del" and not READONLY:
            key = arguments.get("key")
            deleted = client.delete(key)
            return [TextContent(type="text", text=f"Deleted {deleted} key(s)")]

        elif name == "redis_expire" and not READONLY:
            key = arguments.get("key")
            seconds = arguments.get("seconds")
            result = client.expire(key, seconds)
            return [TextContent(type="text", text=f"Expire set: {result}")]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(main())
