"""Streamlit UI for the Gherkin Generator app."""

import streamlit as st
from workflow_service import run_workflow

st.title("Gherkin Generator")

playwright_input = st.text_area("Paste your Playwright record here:")

if st.button("Run Workflow"):
    if playwright_input.strip():
        with st.spinner("Running workflow..."):
            result = run_workflow(playwright_input)
            
            st.subheader("Step 1: Anonymized Record")
            st.code(result["anonymized_record"], language="javascript")
            
            st.subheader("Step 2: Bullet List")
            st.code(result["bullet_list"], language="text")
            
            st.subheader("Step 3: Gherkin Output")
            st.code(result["gherkin"], language="gherkin")
    else:
        st.error("Please enter a Playwright record")
