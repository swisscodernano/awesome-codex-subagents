#!/usr/bin/env python3
"""
Slack MCP Server for Codex CLI
Send notifications and messages to Slack.
"""
import os
import json
import asyncio
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configuration
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
DEFAULT_CHANNEL = os.getenv("SLACK_DEFAULT_CHANNEL", "#alerts")

server = Server("slack-mcp")

@server.list_tools()
async def list_tools():
    """List available tools."""
    return [
        Tool(
            name="slack_send_webhook",
            description="Send a message via Slack webhook (simple)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Message text"},
                    "blocks": {"type": "array", "description": "Slack Block Kit blocks (optional)"}
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="slack_send_message",
            description="Send a message to a channel (requires bot token)",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {"type": "string", "description": "Channel ID or name"},
                    "text": {"type": "string"},
                    "blocks": {"type": "array", "description": "Block Kit blocks"}
                },
                "required": ["channel", "text"]
            }
        ),
        Tool(
            name="slack_alert",
            description="Send a formatted alert message",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Alert title"},
                    "message": {"type": "string", "description": "Alert message"},
                    "severity": {"type": "string", "enum": ["info", "warning", "error", "critical"], "default": "info"},
                    "fields": {"type": "object", "description": "Additional fields as key-value pairs"}
                },
                "required": ["title", "message"]
            }
        ),
        Tool(
            name="slack_incident",
            description="Send an incident notification",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "severity": {"type": "string", "enum": ["P1", "P2", "P3", "P4"], "default": "P3"},
                    "service": {"type": "string", "description": "Affected service"},
                    "runbook_url": {"type": "string", "description": "Link to runbook"}
                },
                "required": ["title", "description"]
            }
        ),
        Tool(
            name="slack_list_channels",
            description="List Slack channels (requires bot token)",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 20}
                }
            }
        )
    ]

def get_severity_emoji(severity: str) -> str:
    """Get emoji for severity level."""
    emojis = {
        "info": ":information_source:",
        "warning": ":warning:",
        "error": ":x:",
        "critical": ":rotating_light:",
        "P1": ":rotating_light:",
        "P2": ":fire:",
        "P3": ":warning:",
        "P4": ":information_source:"
    }
    return emojis.get(severity, ":bell:")

def get_severity_color(severity: str) -> str:
    """Get color for severity level."""
    colors = {
        "info": "#36a64f",
        "warning": "#ffcc00",
        "error": "#ff6600",
        "critical": "#ff0000",
        "P1": "#ff0000",
        "P2": "#ff6600",
        "P3": "#ffcc00",
        "P4": "#36a64f"
    }
    return colors.get(severity, "#808080")

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Execute tool calls."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:

            if name == "slack_send_webhook":
                if not SLACK_WEBHOOK_URL:
                    return [TextContent(type="text", text="Error: SLACK_WEBHOOK_URL not configured")]

                text = arguments.get("text")
                blocks = arguments.get("blocks")

                payload = {"text": text}
                if blocks:
                    payload["blocks"] = blocks

                response = await client.post(SLACK_WEBHOOK_URL, json=payload)
                return [TextContent(type="text", text=f"Sent: {response.status_code} - {response.text}")]

            elif name == "slack_send_message":
                if not SLACK_BOT_TOKEN:
                    return [TextContent(type="text", text="Error: SLACK_BOT_TOKEN not configured")]

                channel = arguments.get("channel")
                text = arguments.get("text")
                blocks = arguments.get("blocks")

                payload = {
                    "channel": channel,
                    "text": text
                }
                if blocks:
                    payload["blocks"] = blocks

                response = await client.post(
                    "https://slack.com/api/chat.postMessage",
                    json=payload,
                    headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
                )
                return [TextContent(type="text", text=json.dumps(response.json(), indent=2))]

            elif name == "slack_alert":
                if not SLACK_WEBHOOK_URL:
                    return [TextContent(type="text", text="Error: SLACK_WEBHOOK_URL not configured")]

                title = arguments.get("title")
                message = arguments.get("message")
                severity = arguments.get("severity", "info")
                fields = arguments.get("fields", {})

                emoji = get_severity_emoji(severity)
                color = get_severity_color(severity)

                blocks = [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": f"{emoji} {title}"}
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": message}
                    }
                ]

                if fields:
                    field_blocks = []
                    for key, value in fields.items():
                        field_blocks.append({
                            "type": "mrkdwn",
                            "text": f"*{key}:*\n{value}"
                        })
                    blocks.append({
                        "type": "section",
                        "fields": field_blocks[:10]  # Max 10 fields
                    })

                payload = {
                    "text": f"{emoji} {title}: {message}",
                    "blocks": blocks,
                    "attachments": [{"color": color, "blocks": []}]
                }

                response = await client.post(SLACK_WEBHOOK_URL, json=payload)
                return [TextContent(type="text", text=f"Alert sent: {response.status_code}")]

            elif name == "slack_incident":
                if not SLACK_WEBHOOK_URL:
                    return [TextContent(type="text", text="Error: SLACK_WEBHOOK_URL not configured")]

                title = arguments.get("title")
                description = arguments.get("description")
                severity = arguments.get("severity", "P3")
                service = arguments.get("service", "Unknown")
                runbook_url = arguments.get("runbook_url", "")

                emoji = get_severity_emoji(severity)
                color = get_severity_color(severity)

                blocks = [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": f"{emoji} INCIDENT: {title}"}
                    },
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Severity:*\n{severity}"},
                            {"type": "mrkdwn", "text": f"*Service:*\n{service}"}
                        ]
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": f"*Description:*\n{description}"}
                    }
                ]

                if runbook_url:
                    blocks.append({
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": f":book: <{runbook_url}|View Runbook>"}
                    })

                payload = {
                    "text": f"{emoji} INCIDENT [{severity}]: {title}",
                    "blocks": blocks,
                    "attachments": [{"color": color, "blocks": []}]
                }

                response = await client.post(SLACK_WEBHOOK_URL, json=payload)
                return [TextContent(type="text", text=f"Incident notification sent: {response.status_code}")]

            elif name == "slack_list_channels":
                if not SLACK_BOT_TOKEN:
                    return [TextContent(type="text", text="Error: SLACK_BOT_TOKEN not configured")]

                limit = arguments.get("limit", 20)
                response = await client.get(
                    "https://slack.com/api/conversations.list",
                    params={"limit": limit, "types": "public_channel,private_channel"},
                    headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
                )
                data = response.json()
                if data.get("ok"):
                    channels = [{"id": c["id"], "name": c["name"]} for c in data.get("channels", [])]
                    return [TextContent(type="text", text=json.dumps(channels, indent=2))]
                return [TextContent(type="text", text=f"Error: {data.get('error')}")]

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
