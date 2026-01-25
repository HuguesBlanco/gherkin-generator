"""LangGraph workflow for converting Playwright recordings to Gherkin tests."""

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


def anonymize_node(state: WorkflowState) -> WorkflowState:
    """Anonymize the Playwright record to remove personal data."""
    # TODO: Implement in Step 5
    state["anonymized_record"] = state["playwright_record"]
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
