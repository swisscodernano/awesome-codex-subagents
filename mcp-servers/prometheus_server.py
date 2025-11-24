#!/usr/bin/env python3
"""
Prometheus MCP Server for Codex CLI
Query metrics and alerts from Prometheus.
"""
import os
import json
import asyncio
from datetime import datetime, timedelta
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configuration
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
TIMEOUT = int(os.getenv("MCP_PROMETHEUS_TIMEOUT", "30"))

server = Server("prometheus-mcp")

@server.list_tools()
async def list_tools():
    """List available tools."""
    return [
        Tool(
            name="prom_query",
            description="Execute an instant PromQL query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "PromQL query expression"},
                    "time": {"type": "string", "description": "Evaluation timestamp (RFC3339 or Unix)"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="prom_query_range",
            description="Execute a range PromQL query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "PromQL query"},
                    "start": {"type": "string", "description": "Start time (RFC3339 or Unix)"},
                    "end": {"type": "string", "description": "End time (RFC3339 or Unix)"},
                    "step": {"type": "string", "description": "Query resolution step (e.g., '15s', '1m')", "default": "1m"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="prom_alerts",
            description="Get current firing alerts",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="prom_rules",
            description="Get alerting and recording rules",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["alert", "record"], "description": "Filter by rule type"}
                }
            }
        ),
        Tool(
            name="prom_targets",
            description="Get scrape targets and their health",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {"type": "string", "enum": ["active", "dropped", "any"], "default": "active"}
                }
            }
        ),
        Tool(
            name="prom_metadata",
            description="Get metric metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "metric": {"type": "string", "description": "Metric name (optional, shows all if omitted)"},
                    "limit": {"type": "integer", "default": 50}
                }
            }
        ),
        Tool(
            name="prom_labels",
            description="Get label names or values",
            inputSchema={
                "type": "object",
                "properties": {
                    "label": {"type": "string", "description": "Label name (if provided, returns values for this label)"}
                }
            }
        ),
        Tool(
            name="prom_series",
            description="Find time series matching selectors",
            inputSchema={
                "type": "object",
                "properties": {
                    "match": {"type": "array", "items": {"type": "string"}, "description": "Series selectors (e.g., ['up', 'http_requests_total{job=\"api\"}'])"}
                },
                "required": ["match"]
            }
        ),
        Tool(
            name="prom_status",
            description="Get Prometheus server status",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["config", "flags", "runtimeinfo", "buildinfo", "tsdb"], "default": "runtimeinfo"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Execute tool calls."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            base_url = PROMETHEUS_URL.rstrip('/')

            if name == "prom_query":
                query = arguments.get("query")
                params = {"query": query}
                if arguments.get("time"):
                    params["time"] = arguments["time"]

                response = await client.get(f"{base_url}/api/v1/query", params=params)
                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "prom_query_range":
                query = arguments.get("query")
                step = arguments.get("step", "1m")

                # Default: last hour
                end = arguments.get("end", datetime.utcnow().isoformat() + "Z")
                start = arguments.get("start", (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z")

                params = {
                    "query": query,
                    "start": start,
                    "end": end,
                    "step": step
                }

                response = await client.get(f"{base_url}/api/v1/query_range", params=params)
                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "prom_alerts":
                response = await client.get(f"{base_url}/api/v1/alerts")
                data = response.json()

                # Simplify output
                if data.get("status") == "success":
                    alerts = data.get("data", {}).get("alerts", [])
                    summary = []
                    for alert in alerts:
                        summary.append({
                            "alertname": alert.get("labels", {}).get("alertname"),
                            "state": alert.get("state"),
                            "severity": alert.get("labels", {}).get("severity"),
                            "instance": alert.get("labels", {}).get("instance"),
                            "summary": alert.get("annotations", {}).get("summary", "")[:100]
                        })
                    return [TextContent(type="text", text=json.dumps({
                        "total": len(alerts),
                        "firing": len([a for a in alerts if a.get("state") == "firing"]),
                        "pending": len([a for a in alerts if a.get("state") == "pending"]),
                        "alerts": summary
                    }, indent=2))]

                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "prom_rules":
                rule_type = arguments.get("type")
                params = {}
                if rule_type:
                    params["type"] = rule_type

                response = await client.get(f"{base_url}/api/v1/rules", params=params)
                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "prom_targets":
                state = arguments.get("state", "active")
                params = {"state": state} if state != "any" else {}

                response = await client.get(f"{base_url}/api/v1/targets", params=params)
                data = response.json()

                # Simplify output
                if data.get("status") == "success":
                    targets = data.get("data", {}).get("activeTargets", [])
                    summary = []
                    for t in targets:
                        summary.append({
                            "job": t.get("labels", {}).get("job"),
                            "instance": t.get("labels", {}).get("instance"),
                            "health": t.get("health"),
                            "lastScrape": t.get("lastScrape"),
                            "scrapeError": t.get("lastError", "")[:100] if t.get("lastError") else ""
                        })
                    return [TextContent(type="text", text=json.dumps({
                        "total": len(targets),
                        "healthy": len([t for t in targets if t.get("health") == "up"]),
                        "unhealthy": len([t for t in targets if t.get("health") != "up"]),
                        "targets": summary
                    }, indent=2))]

                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "prom_metadata":
                metric = arguments.get("metric")
                limit = arguments.get("limit", 50)
                params = {"limit": limit}
                if metric:
                    params["metric"] = metric

                response = await client.get(f"{base_url}/api/v1/metadata", params=params)
                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "prom_labels":
                label = arguments.get("label")

                if label:
                    response = await client.get(f"{base_url}/api/v1/label/{label}/values")
                else:
                    response = await client.get(f"{base_url}/api/v1/labels")

                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "prom_series":
                match = arguments.get("match", [])
                params = [("match[]", m) for m in match]

                response = await client.get(f"{base_url}/api/v1/series", params=params)
                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]

            elif name == "prom_status":
                status_type = arguments.get("type", "runtimeinfo")
                response = await client.get(f"{base_url}/api/v1/status/{status_type}")
                data = response.json()
                return [TextContent(type="text", text=json.dumps(data, indent=2))]

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
