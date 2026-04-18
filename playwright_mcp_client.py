"""MCP client configuration for connecting to the Playwright MCP server via Docker MCP Toolkit."""

from contextlib import asynccontextmanager

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

PLAYWRIGHT_MCP_CONFIG = {
    "playwright": {
        "command": "docker",
        "args": ["run", "-i", "--rm", "mcp/playwright"],
        "transport": "stdio",
    }
}


async def get_playwright_tools():
    """Connect to the Playwright MCP server and return its tools as LangChain tools.

    Each tool call opens a fresh MCP session (and a fresh browser). Fine for
    listing tools or one-shot calls, but NOT for multi-step browsing where
    state (current page, cookies, ...) must persist between calls.
    For stateful browsing, use `playwright_tools_session()` instead.
    """
    client = MultiServerMCPClient(PLAYWRIGHT_MCP_CONFIG)
    tools = await client.get_tools()
    return tools


@asynccontextmanager
async def playwright_tools_session():
    """Open a single Playwright MCP session and yield its tools.

    All tool calls made within the `async with` block share the same browser,
    so navigation and interactions persist across calls.
    """
    client = MultiServerMCPClient(PLAYWRIGHT_MCP_CONFIG)
    async with client.session("playwright") as session:
        tools = await load_mcp_tools(session)
        yield tools
