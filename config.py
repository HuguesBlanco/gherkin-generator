"""Configuration management for the Gherkin Generator app."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_gemini_api_key() -> str:
    """Get the Google Gemini API key from environment variables.
    
    Returns:
        The API key as a string
        
    Raises:
        ValueError: If the API key is not set in the environment
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment variables. "
            "Please create a .env file with your API key. "
            "See .env.example for reference."
        )
    
    return api_key
