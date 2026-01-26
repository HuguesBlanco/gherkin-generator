from workflow import WorkflowState, build_graph


def main():
    """Entry point for the Gherkin Generator app."""
    # Build the workflow graph
    graph = build_graph()
    
    # Example input for testing
    example_playwright = """import { test, expect } from '@playwright/test';

test('login test', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('mySecretPassword123');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page.getByRole('heading')).toContainText('Welcome');
});"""
    
    initial_state: WorkflowState = {
        "playwright_record": example_playwright,
        "anonymized_record": "",
        "bullet_list": "",
        "gherkin": "",
    }
    
    # Run the workflow
    print("Running workflow...")
    result = graph.invoke(initial_state)
    
    print("\n=== Step 6 Verification: Bullet List ===")
    bullet_list = result.get('bullet_list', 'Not generated')
    print(bullet_list)
    
    print("\n=== Step 7 Verification: Gherkin Output ===")
    gherkin_output = result.get('gherkin') or 'Not generated yet'
    print(gherkin_output)
    
    print("\n=== Workflow Status ===")
    print("Workflow completed!")


if __name__ == "__main__":
    main()
