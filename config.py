# config.py
"""
Configuration settings for the People Say AI Search application.

Reads database path and API keys (preferably from environment variables).
"""

import os
from dotenv import load_dotenv

# Constants for database - use absolute path for consistency
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "peoplesay.db")

# Try to load environment variables from .env file, but don't require it
try:
    load_dotenv()
except FileNotFoundError:
    pass  # Silently continue if .env loading fails

# --- LLM Configuration ---
# Fetch the API key from environment variables for security
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Specify the Google Generative AI models to use
# You can experiment with different models available via the API
# e.g., "models/gemini-1.5-pro", "models/gemini-1.0-pro"
SQL_MODEL_NAME = "models/gemini-1.5-flash" # Model for generating SQL
SUMMARY_MODEL_NAME = "models/gemini-1.5-flash" # Model for generating summaries

# --- Input Validation ---
# No need to print a warning here as we'll handle this in the UI
# if not GOOGLE_API_KEY:
#     print("Warning: GOOGLE_API_KEY environment variable not set.")

if not os.path.exists(DB_PATH):
    print(f"Warning: Database file not found at {DB_PATH}")
    # Consider raising an error or handling this case appropriately
    # raise FileNotFoundError(f"Database file not found at {DB_PATH}")

