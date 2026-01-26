"""LangGraph workflow for converting Playwright recordings to Gherkin tests."""

import os
import re
from pathlib import Path
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from config import get_gemini_api_key


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


def load_prompt_template(filename: str, input_variables: list[str]) -> PromptTemplate:
    """Load a prompt template from a text file in the prompts directory.
    
    Args:
        filename: Name of the prompt file (e.g., 'playwright_to_bullet_list.txt')
        input_variables: List of variable names used in the template
        
    Returns:
        PromptTemplate instance
    """
    # Get the directory where this file is located
    current_dir = Path(__file__).parent
    prompt_path = current_dir / "prompts" / filename
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        template_content = f.read()
    
    return PromptTemplate(
        input_variables=input_variables,
        template=template_content
    )


def playwright_to_bullet_list_node(state: WorkflowState) -> WorkflowState:
    """Convert Playwright record to natural language bullet list.
    
    Uses Google Gemini LLM to transform the anonymized Playwright script
    into a bullet list of actions and assertions in natural language.
    """
    # Get the anonymized Playwright record
    playwright_record = state["anonymized_record"]
    
    # Load and format the prompt template
    prompt_template = load_prompt_template(
        "playwright_to_bullet_list.txt",
        input_variables=["playwright_record"]
    )
    formatted_prompt = prompt_template.format(
        playwright_record=playwright_record
    )
    
    # Initialize the LLM with the API key
    # Using gemini-2.5-flash-lite: fastest, cost-efficient, stable model
    # See: https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash-lite
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=get_gemini_api_key(),
        temperature=0,  # Lower temperature for more consistent output
    )
    
    # Call the LLM
    response = llm.invoke(formatted_prompt)
    
    # Extract the bullet list from the response
    # The response is a message object, we need the content
    bullet_list = response.content if hasattr(response, 'content') else str(response)
    
    state["bullet_list"] = bullet_list
    return state


def bullet_list_to_gherkin_node(state: WorkflowState) -> WorkflowState:
    """Convert bullet list to Gherkin format.
    
    Uses Google Gemini LLM to transform the natural language bullet list
    into Gherkin test format.
    """
    # Get the bullet list from state
    bullet_list = state["bullet_list"]
    
    # Load and format the prompt template
    prompt_template = load_prompt_template(
        "bullet_list_to_gherkin.txt",
        input_variables=["bullet_list"]
    )
    formatted_prompt = prompt_template.format(
        bullet_list=bullet_list
    )
    
    # Initialize the LLM with the API key
    # Using gemini-2.5-flash-lite: fastest, cost-efficient, stable model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=get_gemini_api_key(),
        temperature=0,  # Lower temperature for more consistent output
    )
    
    # Call the LLM
    response = llm.invoke(formatted_prompt)
    
    # Extract the Gherkin output from the response
    gherkin = response.content if hasattr(response, 'content') else str(response)
    
    # Clean up the output (remove any leading/trailing whitespace)
    gherkin = gherkin.strip()
    
    state["gherkin"] = gherkin
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
