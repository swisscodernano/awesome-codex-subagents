#!/usr/bin/env python3
"""
PostgreSQL MCP Server for Codex CLI
Enterprise-grade database access with safety controls.
"""
import os
import json
import asyncio
from typing import Any
import psycopg2
from psycopg2.extras import RealDictCursor
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/aiagens")
READONLY = os.getenv("MCP_POSTGRES_READONLY", "true").lower() == "true"
MAX_ROWS = int(os.getenv("MCP_POSTGRES_MAX_ROWS", "1000"))

server = Server("postgres-mcp")

def get_connection():
    """Get database connection."""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

@server.list_tools()
async def list_tools():
    """List available tools."""
    tools = [
        Tool(
            name="pg_query",
            description="Execute a SQL query (SELECT only in readonly mode)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL query to execute"},
                    "params": {"type": "array", "description": "Query parameters", "items": {"type": "string"}}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="pg_schema",
            description="Get database schema information",
            inputSchema={
                "type": "object",
                "properties": {
                    "table": {"type": "string", "description": "Table name (optional, shows all if omitted)"}
                }
            }
        ),
        Tool(
            name="pg_tables",
            description="List all tables in the database",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="pg_stats",
            description="Get table statistics (row counts, sizes)",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

    if not READONLY:
        tools.append(Tool(
            name="pg_execute",
            description="Execute a write query (INSERT, UPDATE, DELETE)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "params": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["query"]
            }
        ))

    return tools

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list:
    """Execute tool calls."""
    try:
        if name == "pg_query":
            return await handle_query(arguments)
        elif name == "pg_schema":
            return await handle_schema(arguments)
        elif name == "pg_tables":
            return await handle_tables()
        elif name == "pg_stats":
            return await handle_stats()
        elif name == "pg_execute" and not READONLY:
            return await handle_execute(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def handle_query(args: dict) -> list:
    """Handle SELECT queries."""
    query = args.get("query", "").strip()
    params = args.get("params", [])

    # Safety check in readonly mode
    if READONLY:
        query_upper = query.upper()
        if not query_upper.startswith("SELECT") and not query_upper.startswith("WITH"):
            return [TextContent(type="text", text="Error: Only SELECT queries allowed in readonly mode")]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchmany(MAX_ROWS)
            result = {
                "rows": [dict(row) for row in rows],
                "row_count": len(rows),
                "truncated": len(rows) >= MAX_ROWS
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

async def handle_schema(args: dict) -> list:
    """Get schema information."""
    table = args.get("table")

    query = """
        SELECT table_name, column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_schema = 'public'
    """
    params = []
    if table:
        query += " AND table_name = %s"
        params.append(table)
    query += " ORDER BY table_name, ordinal_position"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            return [TextContent(type="text", text=json.dumps([dict(r) for r in rows], indent=2))]

async def handle_tables() -> list:
    """List all tables."""
    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            tables = [row["table_name"] for row in cur.fetchall()]
            return [TextContent(type="text", text=json.dumps(tables, indent=2))]

async def handle_stats() -> list:
    """Get table statistics."""
    query = """
        SELECT
            relname as table_name,
            n_live_tup as row_count,
            pg_size_pretty(pg_total_relation_size(relid)) as total_size
        FROM pg_stat_user_tables
        ORDER BY n_live_tup DESC
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [TextContent(type="text", text=json.dumps([dict(r) for r in rows], indent=2))]

async def handle_execute(args: dict) -> list:
    """Handle write queries (when not readonly)."""
    query = args.get("query", "")
    params = args.get("params", [])

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
            return [TextContent(type="text", text=f"Executed successfully. Rows affected: {cur.rowcount}")]

if __name__ == "__main__":
    import sys
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(main())
