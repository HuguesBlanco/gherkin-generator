"""Natural-language browsing agent powered by Playwright MCP tools."""

import asyncio
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from config import get_gemini_api_key
from playwright_mcp_client import playwright_tools_session


SYSTEM_PROMPT = (
    "You are a web-browsing assistant that controls a real browser via "
    "Playwright MCP tools.\n"
    "\n"
    "Allowed tools: browser_navigate, browser_snapshot, browser_click, "
    "browser_type, browser_press_key, browser_wait_for, "
    "browser_navigate_back.\n"
    "Do NOT use browser_evaluate, browser_run_code, or "
    "browser_take_screenshot.\n"
    "\n"
    "Required workflow:\n"
    "1. Call `browser_navigate` with the target URL.\n"
    "2. Call `browser_snapshot` to see the accessibility tree. Each "
    "interactive element has a `ref` string.\n"
    "3. To click or type, call `browser_click` / `browser_type` and "
    "pass BOTH `element` (human-readable description) AND `ref` "
    "(copied EXACTLY from the most recent snapshot). Never invent a "
    "ref and never omit it.\n"
    "4. To submit a search, either set `submit: true` on `browser_type`, "
    "or call `browser_press_key` with `key: \"Enter\"`.\n"
    "5. After any action that changes the page, call `browser_snapshot` "
    "again before your next action.\n"
    "6. Read the answer directly from snapshot text. When you have it, "
    "reply in plain text WITHOUT calling any more tools."
)


def _extract_text(content) -> str:
    """Gemini returns `content` as either a string or a list of parts. Normalize it."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                parts.append(part.get("text", ""))
            elif isinstance(part, str):
                parts.append(part)
        return "\n".join(p for p in parts if p)
    return str(content)


async def answer_question_with_browser(question: str, verbose: bool = False) -> str:
    """Run a browsing agent that uses Playwright MCP tools to answer `question`.

    The MCP session stays open for the whole agent run so the browser state
    (current page, cookies, ...) persists across tool calls.
    """
    async with playwright_tools_session() as tools:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=get_gemini_api_key(),
            temperature=0,
        )

        agent = create_agent(model=llm, tools=tools, system_prompt=SYSTEM_PROMPT)

        final_message = None
        async for event in agent.astream(
            {"messages": [("user", question)]},
            config={"recursion_limit": 50},
            stream_mode="values",
        ):
            messages = event.get("messages", [])
            if not messages:
                continue
            last = messages[-1]
            final_message = last
            if verbose:
                kind = type(last).__name__
                tool_calls = getattr(last, "tool_calls", None)
                if tool_calls:
                    for tc in tool_calls:
                        print(f"[{kind}] -> {tc.get('name')}({tc.get('args')})")
                else:
                    text = _extract_text(last.content)
                    preview = text[:300].replace("\n", " ")
                    print(f"[{kind}] {preview}")

        return _extract_text(final_message.content) if final_message else ""


if __name__ == "__main__":
    demo_question = (
        "Go to the following URL: https://www.wikipedia.org/ "
        "Search for Alan Turing and tell me where he was born."
    )
    answer = asyncio.run(answer_question_with_browser(demo_question, verbose=True))
    print("\n=== FINAL ANSWER ===")
    print(answer)
