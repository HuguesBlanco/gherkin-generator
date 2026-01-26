"""LangGraph workflow for converting Playwright recordings to Gherkin tests."""

import re
from typing import TypedDict
from langgraph.graph import StateGraph, END


# Define the state: what data flows through the graph
class WorkflowState(TypedDict):
    """State that flows through the LangGraph workflow.
    
    Attributes:
        playwright_record: Input Playwright script from the recorder
        anonymized_record: Playwright script after anonymization (removes personal data)
        bullet_list: Natural language bullet list of actions and assertions
        gherkin: Final output in Gherkin format
    """
    playwright_record: str
    anonymized_record: str
    bullet_list: str
    gherkin: str


def build_anonymization_pattern(field_keywords: str) -> str:
    """Build regex pattern to match .fill() calls for specific field types.
    
    The pattern captures three groups:
    1. Everything before the value (getBy* selector and .fill(')
    2. The actual value (what we want to replace)
    3. Everything after the value (closing quote and parenthesis)
    
    Args:
        field_keywords: Keywords to match in the field selector 
                      (e.g., 'password' or 'email|login|username')
        
    Returns:
        Regex pattern string
    """
    # Define regex pattern components
    # Pattern structure: getBy*(...field_name...).fill('value')
    getby_methods = r'getBy(?:Label|Placeholder|Role|Text)'  # Matches getByLabel, getByPlaceholder, etc.
    field_selector = r'\([^)]*'  # Opening parenthesis and field name/selector
    field_closing = r'[^)]*\)'  # Closing parenthesis
    fill_call_start = r'[^.]*\.fill\('  # Any characters before .fill(
    string_quote = r'[\'"]'  # Single or double quote
    string_content = r'[^\'"]+'  # Content inside quotes (what we want to replace)
    string_quote_close = r'[\'"]\)'  # Closing quote and parenthesis
    
    # Wrap field_keywords in non-capturing group to ensure proper alternation
    # This ensures "email|login|username" is treated as one unit, not separate alternatives
    field_keywords_grouped = f'(?:{field_keywords})'
    
    pattern = (
        f'({getby_methods}{field_selector}{field_keywords_grouped}{field_closing}'
        f'{fill_call_start}{string_quote})'
        f'({string_content})'
        f'({string_quote_close})'
    )
    return pattern


def anonymize_node(state: WorkflowState) -> WorkflowState:
    """Anonymize the Playwright record to remove personal data.
    
    This is a very naive implementation that only targets login and password fields
    by looking for .fill() calls that might contain credentials. The goal is to replace
    this with a more robust solution later.
    """
    record = state["playwright_record"]
    
    # Replace password fields first (more specific, so it doesn't conflict with email patterns)
    password_pattern = build_anonymization_pattern('password')
    record = re.sub(
        password_pattern,
        r'\1[PASSWORD]\3',  # Keep groups 1 and 3, replace group 2 (the value) with [PASSWORD]
        record,
        flags=re.IGNORECASE
    )
    
    # Replace email/login/username fields
    email_pattern = build_anonymization_pattern('email|login|username')
    record = re.sub(
        email_pattern,
        r'\1[EMAIL]\3',  # Keep groups 1 and 3, replace group 2 (the value) with [EMAIL]
        record,
        flags=re.IGNORECASE
    )
    
    state["anonymized_record"] = record
    return state


def playwright_to_bullet_list_node(state: WorkflowState) -> WorkflowState:
    """Convert Playwright record to natural language bullet list."""
    # TODO: Implement in Step 6
    state["bullet_list"] = ""
    return state


def bullet_list_to_gherkin_node(state: WorkflowState) -> WorkflowState:
    """Convert bullet list to Gherkin format."""
    # TODO: Implement in Step 7
    state["gherkin"] = ""
    return state


def build_graph() -> StateGraph:
    """Build and return the LangGraph workflow."""
    graph = StateGraph(WorkflowState)
    
    # Add nodes (the processing steps)
    graph.add_node("anonymize", anonymize_node)
    graph.add_node("playwright_to_bullet_list", playwright_to_bullet_list_node)
    graph.add_node("bullet_list_to_gherkin", bullet_list_to_gherkin_node)
    
    # Define the flow: input -> anonymize -> bullet_list -> gherkin -> output
    graph.set_entry_point("anonymize")
    graph.add_edge("anonymize", "playwright_to_bullet_list")
    graph.add_edge("playwright_to_bullet_list", "bullet_list_to_gherkin")
    graph.add_edge("bullet_list_to_gherkin", END)
    
    return graph.compile()
