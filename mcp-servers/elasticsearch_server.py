#!/usr/bin/env python3
"""
Elasticsearch MCP Server for Codex CLI
Search logs, query indices, and analyze data.
"""
import os
import json
import asyncio
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configuration
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USER", "")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD", "")
MAX_RESULTS = int(os.getenv("MCP_ES_MAX_RESULTS", "100"))
TIMEOUT = int(os.getenv("MCP_ES_TIMEOUT", "30"))

server = Server("elasticsearch-mcp")

def get_auth():
    """Get auth tuple if credentials configured."""
    if ELASTICSEARCH_USER and ELASTICSEARCH_PASSWORD:
        return (ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD)
    return None

@server.list_tools()
async def list_tools():
    """List available tools."""
    return [
        Tool(
            name="es_search",
            description="Search documents in an index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string", "description": "Index name or pattern (e.g., 'logs-*')"},
                    "query": {"type": "object", "description": "Elasticsearch query DSL"},
                    "size": {"type": "integer", "default": 10, "description": "Number of results"},
                    "sort": {"type": "array", "description": "Sort specification"},
                    "source": {"type": "array", "description": "Fields to return", "items": {"type": "string"}}
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="es_logs",
            description="Search logs with simple query string",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string", "description": "Index pattern (e.g., 'logs-*')", "default": "logs-*"},
                    "query": {"type": "string", "description": "Simple query string (e.g., 'error AND service:api')"},
                    "time_field": {"type": "string", "default": "@timestamp"},
                    "time_range": {"type": "string", "description": "Time range (e.g., '1h', '24h', '7d')", "default": "1h"},
                    "size": {"type": "integer", "default": 50}
                }
            }
        ),
        Tool(
            name="es_indices",
            description="List indices",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Index pattern", "default": "*"}
                }
            }
        ),
        Tool(
            name="es_index_stats",
            description="Get index statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string", "description": "Index name"}
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="es_mapping",
            description="Get index mapping",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string"}
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="es_count",
            description="Count documents in an index",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string"},
                    "query": {"type": "object", "description": "Optional query to filter"}
                },
                "required": ["index"]
            }
        ),
        Tool(
            name="es_aggregation",
            description="Run an aggregation query",
            inputSchema={
                "type": "object",
                "properties": {
                    "index": {"type": "string"},
                    "aggs": {"type": "object", "description": "Aggregation specification"},
                    "query": {"type": "object", "description": "Optional filter query"},
                    "size": {"type": "integer", "default": 0}
                },
                "required": ["index", "aggs"]
            }
        ),
        Tool(
            name="es_cluster_health",
            description="Get cluster health status",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="es_cluster_stats",
            description="Get cluster statistics",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="es_nodes",
            description="Get node information",
            inputSchema={
                "type": "object",
                "properties": {
                    "info": {"type": "string", "enum": ["stats", "info", "hot_threads"], "default": "stats"}
                }
            }
        )
    ]

def parse_time_range(time_range: str) -> str:
    """Parse time range string to ES format."""
    return f"now-{time_range}"

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Execute tool calls."""
    try:
        auth = get_auth()
        async with httpx.AsyncClient(timeout=TIMEOUT, auth=auth) as client:
            base_url = ELASTICSEARCH_URL.rstrip('/')

            if name == "es_search":
                index = arguments.get("index")
                query = arguments.get("query", {"match_all": {}})
                size = min(arguments.get("size", 10), MAX_RESULTS)
                sort = arguments.get("sort")
                source = arguments.get("source")

                body = {
                    "query": query,
                    "size": size
                }
                if sort:
                    body["sort"] = sort
                if source:
                    body["_source"] = source

                response = await client.post(f"{base_url}/{index}/_search", json=body)
                data = response.json()

                # Simplify response
                if "hits" in data:
                    return [TextContent(type="text", text=json.dumps({
                        "total": data["hits"].get("total", {}).get("value", 0),
                        "took_ms": data.get("took"),
                        "hits": [{"_id": h["_id"], **h.get("_source", {})} for h in data["hits"].get("hits", [])]
                    }, indent=2, default=str))]

                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "es_logs":
                index = arguments.get("index", "logs-*")
                query_string = arguments.get("query", "*")
                time_field = arguments.get("time_field", "@timestamp")
                time_range = arguments.get("time_range", "1h")
                size = min(arguments.get("size", 50), MAX_RESULTS)

                body = {
                    "query": {
                        "bool": {
                            "must": [
                                {"query_string": {"query": query_string}}
                            ],
                            "filter": [
                                {"range": {time_field: {"gte": parse_time_range(time_range)}}}
                            ]
                        }
                    },
                    "sort": [{time_field: "desc"}],
                    "size": size
                }

                response = await client.post(f"{base_url}/{index}/_search", json=body)
                data = response.json()

                if "hits" in data:
                    logs = []
                    for hit in data["hits"].get("hits", []):
                        source = hit.get("_source", {})
                        logs.append({
                            "timestamp": source.get(time_field),
                            "message": source.get("message", source.get("log", "")),
                            "level": source.get("level", source.get("log.level", "")),
                            "service": source.get("service", source.get("service.name", ""))
                        })
                    return [TextContent(type="text", text=json.dumps({
                        "total": data["hits"].get("total", {}).get("value", 0),
                        "logs": logs
                    }, indent=2, default=str))]

                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "es_indices":
                pattern = arguments.get("pattern", "*")
                response = await client.get(f"{base_url}/_cat/indices/{pattern}?format=json&h=index,health,status,docs.count,store.size")
                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "es_index_stats":
                index = arguments.get("index")
                response = await client.get(f"{base_url}/{index}/_stats")
                data = response.json()

                # Simplify
                if "_all" in data:
                    stats = data["_all"]["primaries"]
                    return [TextContent(type="text", text=json.dumps({
                        "docs": stats.get("docs", {}).get("count"),
                        "size_bytes": stats.get("store", {}).get("size_in_bytes"),
                        "indexing_total": stats.get("indexing", {}).get("index_total"),
                        "search_total": stats.get("search", {}).get("query_total")
                    }, indent=2))]

                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "es_mapping":
                index = arguments.get("index")
                response = await client.get(f"{base_url}/{index}/_mapping")
                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "es_count":
                index = arguments.get("index")
                query = arguments.get("query")
                body = {"query": query} if query else None

                if body:
                    response = await client.post(f"{base_url}/{index}/_count", json=body)
                else:
                    response = await client.get(f"{base_url}/{index}/_count")

                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "es_aggregation":
                index = arguments.get("index")
                aggs = arguments.get("aggs")
                query = arguments.get("query", {"match_all": {}})
                size = arguments.get("size", 0)

                body = {
                    "query": query,
                    "aggs": aggs,
                    "size": size
                }

                response = await client.post(f"{base_url}/{index}/_search", json=body)
                data = response.json()

                if "aggregations" in data:
                    return [TextContent(type="text", text=json.dumps({
                        "took_ms": data.get("took"),
                        "aggregations": data["aggregations"]
                    }, indent=2, default=str))]

                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "es_cluster_health":
                response = await client.get(f"{base_url}/_cluster/health")
                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "es_cluster_stats":
                response = await client.get(f"{base_url}/_cluster/stats")
                data = response.json()

                # Simplify
                return [TextContent(type="text", text=json.dumps({
                    "status": data.get("status"),
                    "nodes": data.get("nodes", {}).get("count", {}),
                    "indices": {
                        "count": data.get("indices", {}).get("count"),
                        "docs": data.get("indices", {}).get("docs", {}).get("count"),
                        "store_size": data.get("indices", {}).get("store", {}).get("size_in_bytes")
                    }
                }, indent=2, default=str))]

            elif name == "es_nodes":
                info = arguments.get("info", "stats")
                response = await client.get(f"{base_url}/_nodes/{info}")
                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2, default=str)[:10000])]

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
