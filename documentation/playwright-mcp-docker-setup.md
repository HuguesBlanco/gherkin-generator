# Playwright MCP Server Setup (Docker)

This project uses the [Playwright MCP server running in Docker](https://hub.docker.com/mcp/server/playwright) to let LLMs automate a browser: navigating pages, clicking elements, filling forms, taking screenshots, and more.

The server runs inside a container managed by Docker's **MCP Toolkit** (bundled with Docker Desktop), so you do not need to install Node.js or any browser binaries on the host.

## Prerequisites

**Docker Desktop** must be installed and running.

1. Follow the official guide to [install Docker Desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop).
2. Start Docker Desktop.
3. In a terminal, confirm that Docker is available:
   ```bash
   docker --version
   ```

## Enable the Playwright MCP server

The Playwright MCP server is provided through the MCP Toolkit in Docker Desktop.

1. If **MCP Toolkit** does not appear in the left sidebar of Docker, enable the feature under **Settings**.
2. Open the **MCP Toolkit** section. On the **Catalog** tab, search for **Playwright**, then click **+** to add it.
3. Verify that the image is available locally:
   ```bash
   docker images mcp/playwright
   ```
   The Playwright MCP image should appear in the output.

For more details, see Docker's [MCP Catalog and Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/) documentation.

## Verify the setup

1. From the project root, activate your virtual environment if you have not already done so:
   ```bash
   source venv/bin/activate
   ```
2. Run the test script:
   ```bash
   python test_playwright_mcp.py
   ```
   The script connects to the Playwright MCP server through Docker and lists the available tools. You should see output similar to the following:
   ```
   Connecting to Playwright MCP server via Docker...

   Found 21 tools:

     - browser_click: Perform click on a web page
     - browser_navigate: Navigate to a URL
     - browser_snapshot: Capture accessibility snapshot of the current page
     ...
   ```
   If the list of tools appears, the setup is working correctly.
