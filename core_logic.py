# core_logic.py
"""
Core logic orchestrating the AI search process.

Connects UI input to LLM interface and database handler.
"""

import db_handler # Handles database operations
import llm_inference # Handles LLM API calls
import logging # Use logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_query(user_query: str) -> tuple[str | None, list | None, str | None]:
    """
    Processes the user's natural language query through the entire pipeline.

    1. Generates SQL from the natural language query using the LLM.
    2. Executes the generated SQL query against the database.
    3. Generates a summary from the retrieved data using the LLM.

    Args:
        user_query (str): The natural language question from the user.

    Returns:
        tuple[str | None, list | None, str | None]: A tuple containing:
            - str: The generated summary text, or an error/status message.
            - list: A list of dictionaries representing the source data rows, or None/[] on error/no data.
            - str: The generated SQL query (for display/debugging), or None on failure.
    """
    logging.info(f"Processing user query: {user_query}")

    # --- Step 1: Generate SQL Query ---
    sql_query = llm_inference.generate_sql_from_query(user_query)

    if not sql_query:
        logging.error("Failed to generate SQL query.")
        return "Error: Could not generate the database query.", [], None # Return error, empty list, no SQL

    logging.info(f"Generated SQL: {sql_query}")

    # --- Step 2: Execute SQL Query ---
    # The db_handler function returns an empty DataFrame on error or no results
    retrieved_data_df = db_handler.execute_sql_query(sql_query)

    # Check if DataFrame is empty (could be error or genuinely no results)
    if retrieved_data_df.empty:
        # Check if the SQL query itself was valid but returned no rows
        # (This check might be refined based on db_handler's error reporting)
        logging.warning("SQL query executed but returned no data.")
        # Return specific message for no data found
        return "No data found matching your query.", [], sql_query # Return message, empty list, and the SQL used

    logging.info(f"Retrieved {len(retrieved_data_df)} data entries from database.")

    # --- Step 3: Generate Summary ---
    # llm_inference handles the case where the DataFrame is empty, but we check again for clarity
    if not retrieved_data_df.empty:
        summary, sources = llm_inference.generate_summary_from_data(user_query, retrieved_data_df)

        if summary is None and sources is None: # Indicates a failure in summary generation API call
             logging.error("Failed to generate summary from data.")
             # Return error message, empty sources list, and the SQL query
             return "Error: Could not generate the summary from the retrieved data.", [], sql_query
        elif sources is None: # Indicates an error message was returned instead of summary
            logging.error(f"Summary generation returned an error message: {summary}")
            return summary, [], sql_query # Return the error message from LLM interface
        else:
            logging.info("Summary generated successfully.")
            # Return the summary, the list of source dicts, and the SQL query
            return summary, sources, sql_query
    else:
        # This case should technically be caught earlier, but included for completeness
        logging.warning("No data available to generate summary (redundant check).")
        return "No data found matching your query.", [], sql_query


