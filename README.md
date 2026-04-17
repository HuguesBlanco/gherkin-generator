# Gherkin Generator

A Python proof of concept built with LangGraph to automate Gherkin test generation.

## 1. One-time setup

Run these steps once after cloning the repository.

### 1.1 Prerequisite (Debian): Python `venv` support

Install virtual environment support for Python, if it is not already available:
```bash
sudo apt update
sudo apt install python3-venv
```

### 1.2 Create a virtual environment

```bash
python3 -m venv venv
```

### 1.3 Install dependencies

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the project in editable mode (`-e`) so local code changes are immediately available without reinstalling:

```bash
pip install -e .
```

### 1.4 Run the Playwright MCP server (Docker)

Follow **[Playwright MCP Docker setup](documentation/playwright-mcp-docker-setup.md)** to start the Playwright MCP server with Docker.

## 2. Daily workflow

Use these steps each time you open a new terminal for this project.

### 2.1 Activate the environment

```bash
source venv/bin/activate
```

### 2.2 Run the app

```bash
python main.py
```

The Streamlit UI opens automatically in your browser.
