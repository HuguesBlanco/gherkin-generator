"""MCP client configuration for connecting to the Playwright MCP server via Docker MCP Toolkit."""

from langchain_mcp_adapters.client import MultiServerMCPClient

PLAYWRIGHT_MCP_CONFIG = {
    "playwright": {
        "command": "docker",
        "args": ["run", "-i", "--rm", "mcp/playwright"],
        "transport": "stdio",
    }
}


async def get_playwright_tools():
    """Connect to the Playwright MCP server and return its tools as LangChain tools."""
    client = MultiServerMCPClient(PLAYWRIGHT_MCP_CONFIG)
    tools = await client.get_tools()
    return tools
