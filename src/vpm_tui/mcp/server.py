"""MCP server entrypoint."""

import asyncio

from mcp.server.fastmcp import FastMCP

from vpm_tui.mcp.tools import register_tools

mcp_server = FastMCP("vpm_tui")
register_tools(mcp_server)


def main() -> None:
    asyncio.run(mcp_server.run_stdio_async())
