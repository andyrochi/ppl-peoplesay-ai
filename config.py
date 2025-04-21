# config.py
"""
Configuration settings for the People Say AI Search application.

Reads database path and API keys (preferably from environment variables).
"""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
# Create a .env file in the same directory with GOOGLE_API_KEY=YOUR_API_KEY
load_dotenv()

# --- Database Configuration ---
DB_PATH = "peoplesay.db" # Path to your SQLite database file

# --- LLM Configuration ---
# Fetch the API key from environment variables for security
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Specify the Google Generative AI models to use
# You can experiment with different models available via the API
# e.g., "models/gemini-1.5-pro", "models/gemini-1.0-pro"
SQL_MODEL_NAME = "models/gemini-1.5-flash" # Model for generating SQL
SUMMARY_MODEL_NAME = "models/gemini-1.5-flash" # Model for generating summaries

# --- Input Validation ---
if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY environment variable not set.")
    # Consider raising an error or exiting if the API key is essential
    # raise ValueError("GOOGLE_API_KEY environment variable is required.")

if not os.path.exists(DB_PATH):
    print(f"Warning: Database file not found at {DB_PATH}")
    # Consider raising an error or handling this case appropriately
    # raise FileNotFoundError(f"Database file not found at {DB_PATH}")

