"""Streamlit UI for the Gherkin Generator app."""

import streamlit as st
from workflow_service import run_workflow

st.title("Gherkin Generator")

playwright_input = st.text_area("Paste your Playwright record here:")

if st.button("Run Workflow"):
    if playwright_input.strip():
        with st.spinner("Running workflow..."):
            result = run_workflow(playwright_input)
            st.code(result, language="gherkin")
    else:
        st.error("Please enter a Playwright record")
