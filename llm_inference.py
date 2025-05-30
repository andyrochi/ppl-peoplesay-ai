# llm_interface.py
"""
Handles interactions with the Google Generative AI API.

Provides functions to:
1. Generate SQL queries from natural language user questions.
2. Generate summaries from data retrieved from the database.
"""

import google.generativeai as genai
import pandas as pd
import config # Import configuration (API key, model names)
import prompts # Import prompt templates
import logging # Use logging for better error/info reporting
import re # For potential SQL cleaning
import requests # For API key verification

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Function to verify Google API Key ---
def verify_google_api_key(api_key):
    """
    Verifies if the provided Google API key is valid by making a test request.
    Returns True if valid, False otherwise.
    """
    try:
        # Small test request to the Generative Language API
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            return True
        else:
            error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            logging.warning(f"API key verification failed: {error_msg}")
            return False
    except Exception as e:
        logging.error(f"Error verifying API key: {e}")
        return False

# Function to configure/reconfigure the API with a new key
def configure_genai(api_key=None):
    """Configure Google Generative AI with the provided API key or from config."""
    try:
        # Use provided API key or fall back to config
        key_to_use = api_key or config.GOOGLE_API_KEY
        
        if not key_to_use:
            logging.warning("No API key provided. Attempting to run without API key.")
            return False
        else:
            if not verify_google_api_key(key_to_use):
                logging.error("Invalid Google API Key provided.")
                return False
                
            genai.configure(api_key=key_to_use)
            logging.info("Google Generative AI SDK configured successfully.")
            return True
    except Exception as e:
        logging.error(f"Failed to configure Google Generative AI SDK: {e}", exc_info=True)
        return False

# --- SQL Generation ---
def generate_sql_from_query(user_query: str, api_key=None, model_name=None) -> str | None:
    """
    Generates an SQL query from a natural language user query using the configured LLM.

    Args:
        user_query (str): The natural language question from the user.
        api_key (str, optional): The API key to use.
        model_name (str, optional): The name of the model to use.

    Returns:
        str | None: The generated SQL query string, or None if generation fails or
                    API key is not configured.
    """
    if not api_key:
        logging.error("Cannot generate SQL: No API key provided")
        return None
    # Attempt to configure with the provided API key
    if not configure_genai(api_key):
        logging.error("Cannot generate SQL: Invalid or missing API key.")
        return None
    
    if not user_query or not isinstance(user_query, str):
        logging.warning("Cannot generate SQL: Invalid user query provided.")
        return None

    try:
        # Initialize the specific model for SQL generation
        model_to_use = model_name or config.SQL_MODEL_NAME
        model = genai.GenerativeModel(model_to_use)
        logging.info(f"Using model {model_to_use} for SQL generation.")

        # Format the prompt with the user's query
        prompt = prompts.SQL_GENERATION_PROMPT_TEMPLATE.format(user_query=user_query)
        logging.info("Sending request to LLM for SQL generation...")
        # print(f"DEBUG SQL Prompt:\n{prompt[:1000]}...") # Uncomment for debugging long prompts

        # Make the API call
        response = model.generate_content(prompt)

        # --- Response Processing ---
        if not response.text:
             logging.warning("LLM response for SQL generation was empty.")
             return None

        # Extract the SQL query - the prompt asks for ONLY SQL
        sql_query = response.text.strip()

        # Basic cleaning: Remove potential markdown backticks if the LLM ignored instructions
        sql_query = re.sub(r"^```sql\s*", "", sql_query, flags=re.IGNORECASE)
        sql_query = re.sub(r"\s*```$", "", sql_query)
        sql_query = sql_query.strip() # Remove leading/trailing whitespace

        # Basic validation (can be expanded)
        if "SELECT" not in sql_query.upper():
            logging.warning(f"Generated text does not appear to be a valid SELECT SQL query: {sql_query}")
            # Optionally return None or try to handle differently
            return None # Returning None as it likely failed

        logging.info(f"Successfully generated SQL query: {sql_query[:500]}...")
        return sql_query

    except Exception as e:
        # Catch potential API errors, configuration issues, etc.
        logging.error(f"Error generating SQL query via LLM: {e}", exc_info=True)
        return None

# --- Summary Generation ---
def generate_summary_from_data(user_query: str, retrieved_data_df: pd.DataFrame, 
                               template_key: str = "Thematic Analysis",
                               api_key=None, model_name=None) -> tuple[str | None, list | None]:
    """
    Generates a summary from the retrieved data DataFrame using the configured LLM.

    Args:
        user_query (str): The original user query (for context).
        retrieved_data_df (pd.DataFrame): DataFrame containing the data retrieved
                                         by the SQL query. Must include 'data_unit'
                                         and 'participant_name' columns.
        template_key (str): The key of the template to use from prompts.SUMMARY_TEMPLATES.
                           Defaults to "Thematic Analysis".
        

    Returns:
        tuple[str | None, list | None]: A tuple containing:
            - str: The generated summary text.
            - list: A list of dictionaries, where each dictionary represents a source row
                    from the input DataFrame.
            Returns (None, None) if summarization fails, data is empty, or API key is missing.
            Returns (error_message_str, None) if an error occurs during generation.
    """
    # Attempt to configure with the provided API key

    if not api_key:
        logging.error("Cannot generate summary: No API key provided")
        return "API key error: Please provide a valid API key.", None

    if not configure_genai(api_key):
        logging.error("Cannot generate summary: Invalid or missing API key.")
        return "API key error: Failed to authenticate with the provided key.", None

    if retrieved_data_df.empty:
        logging.info("No data provided to generate summary.")
        # Return specific message instead of None to indicate no data vs. error
        return "No relevant data found to summarize.", []

    # Validate required columns exist
    required_columns = ['data_unit','data_unit_title', 'participant_name']
    if not all(col in retrieved_data_df.columns for col in required_columns):
        logging.error(f"Retrieved data DataFrame is missing required columns: {required_columns}")
        missing = [col for col in required_columns if col not in retrieved_data_df.columns]
        return f"Internal Error: Data processing failed (missing columns: {missing}).", None

    # --- Format Data for Prompt ---
    # Create a string representation of the data for the LLM prompt.
    # Use 'data_unit' as the citation ID as requested.
    data_context_parts = []
    sources_list = [] # Keep track of the original data rows for display later
    for index, row in retrieved_data_df.iterrows():
        # Use data_unit as the primary identifier/excerpt content
        source_id = row['data_unit_title']
        participant = row['participant_name']
        excerpt = row['data_unit'] # Using data_unit as the excerpt text

        # --- Add Metadata Extraction ---
        # Extract relevant metadata fields, handling potential missing values
        age = row.get('age', 'N/A')
        gender = row.get('gender', 'N/A')
        race_ethnicity = row.get('participant_race_ethnicity', 'N/A') # Assuming this column name based on app.py
        location = row.get('location_type', 'N/A')
        state = row.get('state', 'N/A')
        income = row.get('income_range_fpl', 'N/A')
        insurance = row.get('participant_insurance', 'N/A') # Assuming this column name based on app.py
        language = row.get('language', 'N/A')
        participant_type = row.get('participant_type', 'N/A')

        # Format metadata string
        metadata_str = (
            f"Participant Type: {participant_type}\n"
            f"Age: {age}\n"
            f"Gender: {gender}\n"
            f"Race/Ethnicity: {race_ethnicity}\n"
            f"Language: {language}\n"
            f"Location: {location} ({state})\n"
            f"Income (FPL): {income}\n"
            f"Insurance: {insurance}"
        )

        # Format for the prompt, now including metadata
        data_context_parts.append(
            f"Source ID: [{source_id}]\n"
            f"Participant: {participant}\n"
            f"Metadata:\n{metadata_str}\n"
            f"Excerpt: {excerpt}\n"
        )
        
        # Add the full row (as dict) to sources list
        sources_list.append(row.to_dict())

    if not data_context_parts:
        logging.warning("Could not format any data for the summarization prompt.")
        return "Could not prepare data for summarization.", None

    data_context_string = "\n---\n".join(data_context_parts) # Separate entries clearly

    try:
        # Initialize the specific model for summarization
        model_to_use = model_name or config.SUMMARY_MODEL_NAME
        model = genai.GenerativeModel(model_to_use)
        logging.info(f"Using model {model_to_use} for summarization with {template_key} template.")

        # Get the appropriate template
        template = prompts.SUMMARY_TEMPLATES.get(template_key, prompts.DEFAULT_SUMMARY_TEMPLATE)

        # Format the prompt
        prompt = template.format(
            user_query=user_query,
            retrieved_data=data_context_string
        )
        logging.info("Sending request to LLM for summary generation...")
        # print(f"DEBUG Summary Prompt:\n{prompt[:1000]}...") # Uncomment for debugging

        # Make the API call
        response = model.generate_content(prompt)

        if not response.text:
             logging.warning("LLM response for summary generation was empty.")
             # Return specific message instead of None
             return "The AI failed to generate a summary based on the data.", sources_list

        summary_text = response.text.strip()
        logging.info("Successfully generated summary.")
        return summary_text, sources_list # Return summary and the list of source dicts

    except Exception as e:
        logging.error(f"Error generating summary via LLM: {e}", exc_info=True)
        # Return error message and None for sources
        return f"An error occurred while generating the summary: {e}", None

