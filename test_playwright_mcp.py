"""Quick verification script: connects to Playwright MCP server and lists available tools."""

import asyncio
from playwright_mcp_client import get_playwright_tools


async def main():
    print("Connecting to Playwright MCP server via Docker...")
    tools = await get_playwright_tools()
    print(f"\nFound {len(tools)} tools:\n")
    for tool in tools:
        name = tool.name
        description = (tool.description or "").split("\n")[0]
        print(f"  - {name}: {description}")


if __name__ == "__main__":
    asyncio.run(main())
