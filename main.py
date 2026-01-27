"""Main entry point for the Gherkin Generator app.

Launches the Streamlit UI.
"""

import subprocess
import sys


def main():
    """Launch the Streamlit app."""
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        # User pressed Ctrl+C - exit cleanly
        sys.exit(0)


if __name__ == "__main__":
    main()
