#!/usr/bin/env python3
"""
GitHub MCP Server for Codex CLI
Uses gh CLI for GitHub operations.
"""
import os
import json
import asyncio
import subprocess
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("github-mcp")

def run_gh(args: list) -> tuple[str, int]:
    """Run gh CLI command."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout or result.stderr, result.returncode
    except Exception as e:
        return str(e), 1

@server.list_tools()
async def list_tools():
    """List available tools."""
    return [
        Tool(
            name="gh_pr_list",
            description="List pull requests",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "Repository (owner/repo)"},
                    "state": {"type": "string", "enum": ["open", "closed", "merged", "all"], "default": "open"},
                    "limit": {"type": "integer", "default": 10}
                }
            }
        ),
        Tool(
            name="gh_pr_view",
            description="View a specific pull request",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {"type": "string"},
                    "number": {"type": "integer", "description": "PR number"}
                },
                "required": ["number"]
            }
        ),
        Tool(
            name="gh_issue_list",
            description="List issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {"type": "string"},
                    "state": {"type": "string", "enum": ["open", "closed", "all"], "default": "open"},
                    "limit": {"type": "integer", "default": 10}
                }
            }
        ),
        Tool(
            name="gh_issue_view",
            description="View a specific issue",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {"type": "string"},
                    "number": {"type": "integer"}
                },
                "required": ["number"]
            }
        ),
        Tool(
            name="gh_repo_view",
            description="View repository information",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {"type": "string", "description": "Repository (owner/repo)"}
                }
            }
        ),
        Tool(
            name="gh_workflow_list",
            description="List GitHub Actions workflows",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {"type": "string"}
                }
            }
        ),
        Tool(
            name="gh_run_list",
            description="List recent workflow runs",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                }
            }
        ),
        Tool(
            name="gh_api",
            description="Make a GitHub API request",
            inputSchema={
                "type": "object",
                "properties": {
                    "endpoint": {"type": "string", "description": "API endpoint (e.g., /repos/owner/repo)"},
                    "method": {"type": "string", "enum": ["GET", "POST", "PATCH", "DELETE"], "default": "GET"}
                },
                "required": ["endpoint"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Execute tool calls."""
    try:
        repo = arguments.get("repo", "")
        repo_args = ["-R", repo] if repo else []

        if name == "gh_pr_list":
            limit = arguments.get("limit", 10)
            state = arguments.get("state", "open")
            output, code = run_gh(["pr", "list"] + repo_args + ["--limit", str(limit), "--state", state, "--json", "number,title,state,author,createdAt"])

        elif name == "gh_pr_view":
            number = arguments.get("number")
            output, code = run_gh(["pr", "view", str(number)] + repo_args + ["--json", "number,title,body,state,author,additions,deletions,files"])

        elif name == "gh_issue_list":
            limit = arguments.get("limit", 10)
            state = arguments.get("state", "open")
            output, code = run_gh(["issue", "list"] + repo_args + ["--limit", str(limit), "--state", state, "--json", "number,title,state,author,createdAt"])

        elif name == "gh_issue_view":
            number = arguments.get("number")
            output, code = run_gh(["issue", "view", str(number)] + repo_args + ["--json", "number,title,body,state,author,comments"])

        elif name == "gh_repo_view":
            output, code = run_gh(["repo", "view"] + repo_args + ["--json", "name,description,stargazerCount,forkCount,isPrivate,defaultBranchRef"])

        elif name == "gh_workflow_list":
            output, code = run_gh(["workflow", "list"] + repo_args + ["--json", "name,state"])

        elif name == "gh_run_list":
            limit = arguments.get("limit", 10)
            output, code = run_gh(["run", "list"] + repo_args + ["--limit", str(limit), "--json", "databaseId,displayTitle,status,conclusion,createdAt"])

        elif name == "gh_api":
            endpoint = arguments.get("endpoint")
            method = arguments.get("method", "GET")
            output, code = run_gh(["api", endpoint, "-X", method])

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        if code != 0:
            return [TextContent(type="text", text=f"Error: {output}")]

        return [TextContent(type="text", text=output)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(main())
