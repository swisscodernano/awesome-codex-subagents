#!/usr/bin/env python3
"""
Docker MCP Server for Codex CLI
Container management and monitoring.
"""
import os
import json
import asyncio
import subprocess
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configuration
READONLY = os.getenv("MCP_DOCKER_READONLY", "true").lower() == "true"

server = Server("docker-mcp")

def run_docker(args: list, timeout: int = 30) -> tuple[str, int]:
    """Run docker command."""
    try:
        result = subprocess.run(
            ["docker"] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout or result.stderr, result.returncode
    except Exception as e:
        return str(e), 1

@server.list_tools()
async def list_tools():
    """List available tools."""
    tools = [
        Tool(
            name="docker_ps",
            description="List running containers",
            inputSchema={
                "type": "object",
                "properties": {
                    "all": {"type": "boolean", "description": "Show all containers (including stopped)", "default": False}
                }
            }
        ),
        Tool(
            name="docker_images",
            description="List Docker images",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="docker_logs",
            description="Get container logs",
            inputSchema={
                "type": "object",
                "properties": {
                    "container": {"type": "string", "description": "Container ID or name"},
                    "tail": {"type": "integer", "description": "Number of lines", "default": 100}
                },
                "required": ["container"]
            }
        ),
        Tool(
            name="docker_inspect",
            description="Inspect a container or image",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Container/image ID or name"}
                },
                "required": ["target"]
            }
        ),
        Tool(
            name="docker_stats",
            description="Get container resource usage",
            inputSchema={
                "type": "object",
                "properties": {
                    "container": {"type": "string", "description": "Container ID (optional, shows all if omitted)"}
                }
            }
        ),
        Tool(
            name="docker_top",
            description="Show running processes in container",
            inputSchema={
                "type": "object",
                "properties": {
                    "container": {"type": "string"}
                },
                "required": ["container"]
            }
        ),
        Tool(
            name="docker_networks",
            description="List Docker networks",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="docker_volumes",
            description="List Docker volumes",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="docker_system_df",
            description="Show Docker disk usage",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="docker_version",
            description="Show Docker version info",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

    if not READONLY:
        tools.extend([
            Tool(
                name="docker_start",
                description="Start a stopped container",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "container": {"type": "string"}
                    },
                    "required": ["container"]
                }
            ),
            Tool(
                name="docker_stop",
                description="Stop a running container",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "container": {"type": "string"},
                        "timeout": {"type": "integer", "default": 10}
                    },
                    "required": ["container"]
                }
            ),
            Tool(
                name="docker_restart",
                description="Restart a container",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "container": {"type": "string"}
                    },
                    "required": ["container"]
                }
            ),
            Tool(
                name="docker_exec",
                description="Execute command in container",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "container": {"type": "string"},
                        "command": {"type": "string"}
                    },
                    "required": ["container", "command"]
                }
            )
        ])

    return tools

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Execute tool calls."""
    try:
        if name == "docker_ps":
            all_containers = arguments.get("all", False)
            args = ["ps", "--format", "json"]
            if all_containers:
                args.append("-a")
            output, code = run_docker(args)

            # Parse JSON lines output
            containers = []
            for line in output.strip().split('\n'):
                if line:
                    try:
                        containers.append(json.loads(line))
                    except:
                        pass
            return [TextContent(type="text", text=json.dumps(containers, indent=2))]

        elif name == "docker_images":
            output, code = run_docker(["images", "--format", "json"])
            images = []
            for line in output.strip().split('\n'):
                if line:
                    try:
                        images.append(json.loads(line))
                    except:
                        pass
            return [TextContent(type="text", text=json.dumps(images, indent=2))]

        elif name == "docker_logs":
            container = arguments.get("container")
            tail = arguments.get("tail", 100)
            output, code = run_docker(["logs", "--tail", str(tail), container])
            return [TextContent(type="text", text=output)]

        elif name == "docker_inspect":
            target = arguments.get("target")
            output, code = run_docker(["inspect", target])
            return [TextContent(type="text", text=output)]

        elif name == "docker_stats":
            container = arguments.get("container")
            args = ["stats", "--no-stream", "--format", "json"]
            if container:
                args.append(container)
            output, code = run_docker(args)
            stats = []
            for line in output.strip().split('\n'):
                if line:
                    try:
                        stats.append(json.loads(line))
                    except:
                        pass
            return [TextContent(type="text", text=json.dumps(stats, indent=2))]

        elif name == "docker_top":
            container = arguments.get("container")
            output, code = run_docker(["top", container])
            return [TextContent(type="text", text=output)]

        elif name == "docker_networks":
            output, code = run_docker(["network", "ls", "--format", "json"])
            networks = []
            for line in output.strip().split('\n'):
                if line:
                    try:
                        networks.append(json.loads(line))
                    except:
                        pass
            return [TextContent(type="text", text=json.dumps(networks, indent=2))]

        elif name == "docker_volumes":
            output, code = run_docker(["volume", "ls", "--format", "json"])
            volumes = []
            for line in output.strip().split('\n'):
                if line:
                    try:
                        volumes.append(json.loads(line))
                    except:
                        pass
            return [TextContent(type="text", text=json.dumps(volumes, indent=2))]

        elif name == "docker_system_df":
            output, code = run_docker(["system", "df", "-v"])
            return [TextContent(type="text", text=output)]

        elif name == "docker_version":
            output, code = run_docker(["version", "--format", "json"])
            return [TextContent(type="text", text=output)]

        # Write operations
        elif name == "docker_start" and not READONLY:
            container = arguments.get("container")
            output, code = run_docker(["start", container])
            return [TextContent(type="text", text=f"Started: {output}" if code == 0 else f"Error: {output}")]

        elif name == "docker_stop" and not READONLY:
            container = arguments.get("container")
            timeout = arguments.get("timeout", 10)
            output, code = run_docker(["stop", "-t", str(timeout), container])
            return [TextContent(type="text", text=f"Stopped: {output}" if code == 0 else f"Error: {output}")]

        elif name == "docker_restart" and not READONLY:
            container = arguments.get("container")
            output, code = run_docker(["restart", container])
            return [TextContent(type="text", text=f"Restarted: {output}" if code == 0 else f"Error: {output}")]

        elif name == "docker_exec" and not READONLY:
            container = arguments.get("container")
            command = arguments.get("command")
            output, code = run_docker(["exec", container, "sh", "-c", command], timeout=60)
            return [TextContent(type="text", text=output)]

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
