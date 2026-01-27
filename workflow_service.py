"""Service layer for executing the workflow.

This module provides a simple interface to run the workflow,
keeping UI concerns separate from the workflow logic.
"""

from workflow import build_graph, WorkflowState


def run_workflow(playwright_record: str) -> str:
    """Run the workflow and return the Gherkin result.
    
    Args:
        playwright_record: The Playwright script to convert
        
    Returns:
        The generated Gherkin test as a string
    """
    graph = build_graph()
    initial_state: WorkflowState = {
        "playwright_record": playwright_record,
        "anonymized_record": "",
        "bullet_list": "",
        "gherkin": "",
    }
    result = graph.invoke(initial_state)
    return result.get("gherkin", "")
