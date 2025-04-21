# db_handler.py
"""
Handles interactions with the SQLite database (`peoplesay.db`).

Provides functions to establish a connection and execute SQL queries.
"""

import sqlite3
import pandas as pd
import config # Use config module to get DB path
import logging # Use logging for better error reporting
import os # For checking file existence

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database specified in config.
    Configures the connection to return rows as dictionary-like objects.

    Returns:
        sqlite3.Connection: Database connection object.
        None: If the database file doesn't exist or connection fails.
    """
    if not config.DB_PATH or not isinstance(config.DB_PATH, str):
         logging.error("Database path not configured correctly in config.py.")
         return None

    if not os.path.exists(config.DB_PATH):
        logging.error(f"Database file not found at path: {config.DB_PATH}")
        return None

    try:
        conn = sqlite3.connect(config.DB_PATH)
        # Use sqlite3.Row factory to access columns by name (like a dictionary)
        conn.row_factory = sqlite3.Row
        logging.info(f"Successfully connected to database: {config.DB_PATH}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}", exc_info=True)
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during DB connection: {e}", exc_info=True)
        return None


def execute_sql_query(sql_query: str) -> pd.DataFrame:
    """
    Executes a given SQL SELECT query against the database.

    Args:
        sql_query (str): The SQL query string to execute.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the query results.
                      Returns an empty DataFrame if the query fails,
                      returns no results, or if the input is invalid.
    """
    if not sql_query or not isinstance(sql_query, str) or "SELECT" not in sql_query.upper():
        logging.warning(f"Invalid or non-SELECT SQL query provided: {sql_query}")
        return pd.DataFrame() # Return empty DataFrame for invalid input

    logging.info(f"Executing SQL query: {sql_query[:500]}...") # Log truncated query

    conn = get_db_connection()
    if conn is None:
        logging.error("Failed to execute SQL query due to database connection failure.")
        return pd.DataFrame() # Return empty DataFrame if connection failed

    try:
        # Use pandas read_sql_query for convenience
        df = pd.read_sql_query(sql_query, conn)
        logging.info(f"SQL query executed successfully, {len(df)} rows returned.")
        return df
    except pd.io.sql.DatabaseError as e:
        # Catch pandas-specific database errors which might wrap sqlite3 errors
        logging.error(f"Pandas Database error during SQL execution: {e}", exc_info=True)
        logging.error(f"Failed Query: {sql_query}")
        return pd.DataFrame()
    except sqlite3.Error as e:
        # Catch underlying sqlite3 errors if not caught by pandas
        logging.error(f"SQLite Database error during SQL execution: {e}", exc_info=True)
        logging.error(f"Failed Query: {sql_query}")
        return pd.DataFrame()
    except Exception as e:
        # Catch any other unexpected errors
        logging.error(f"An unexpected error occurred during SQL execution: {e}", exc_info=True)
        logging.error(f"Failed Query: {sql_query}")
        return pd.DataFrame()
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()
            logging.info("Database connection closed.")

