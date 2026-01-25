from workflow import WorkflowState, build_graph


def main():
    """Entry point for the Gherkin Generator app."""
    # Build the workflow graph
    graph = build_graph()
    
    # Example input (will be replaced with actual user input later)
    initial_state: WorkflowState = {
        "playwright_record": "import { test, expect } from '@playwright/test';",
        "anonymized_record": "",
        "bullet_list": "",
        "gherkin": "",
    }
    
    # Run the workflow
    result = graph.invoke(initial_state)
    
    print("Workflow completed!")
    gherkin_output = result.get('gherkin') or 'Not generated yet'
    print(f"Gherkin output: {gherkin_output}")


if __name__ == "__main__":
    main()
