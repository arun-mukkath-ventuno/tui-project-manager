"""Tests for MCP tools."""

import asyncio

from mcp.server.fastmcp import FastMCP

from vpm_tui.mcp.tools import register_tools


def test_register_tools() -> None:
    mcp = FastMCP("test")
    register_tools(mcp)

    async def _get_tools():
        return await mcp.list_tools()

    tools = asyncio.run(_get_tools())
    tool_names = [t.name for t in tools]
    assert "list_projects" in tool_names
    assert "get_project_detail" in tool_names
    assert "list_tasks" in tool_names
    assert "generate_summary" in tool_names
    assert "refresh_source_data" in tool_names
