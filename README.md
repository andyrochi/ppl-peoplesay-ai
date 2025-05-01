# People Say AI Search Tool 🗣️

## Introduction

This application provides a user-friendly interface to query the "People Say" database using natural language. It leverages Google's Generative AI models to understand user questions, generate appropriate SQL queries, retrieve relevant data excerpts from the database, and synthesize the findings into a concise summary with citations.

The tool is designed to help researchers, policymakers, and anyone interested in understanding the experiences of older adults access insights from the "People Say" qualitative data archive more easily.

## Features

*   **Natural Language Querying:** Ask questions in plain English instead of writing complex SQL.
*   **AI-Powered Summarization:** Get summaries of relevant database excerpts tailored to your query.
*   **Source Citation:** Summaries include references to the specific data excerpts used.
*   **Multiple Analysis Types:** Choose from different analytical frames (e.g., Thematic Analysis, Narrative Analysis) to guide the AI's summarization process.
*   **Database Interaction:** Automatically generates and executes SQL queries against the local SQLite database.
*   **Transparency:** View the AI-generated SQL query used to retrieve data.

## Getting Started

Follow these steps to set up and run the application locally.

### Prerequisites

*   Python 3.8 or higher
*   Git (for cloning the repository)
*   Access to a Google API Key with the Generative Language API enabled. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url> # Replace with your actual repo URL
    cd <repository-directory>       # cd into the project folder
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    Make sure you have a `requirements.txt` file with the necessary libraries. If not, create one containing at least:
    ```txt
    # filepath: requirements.txt
    streamlit
    google-generativeai
    # Add any other specific libraries used, e.g., pandas if used in core_logic
    ```
    Then install:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    This will open the application in your default web browser.

2.  **Enter your Google API Key:**
    The first time you run the app (or start a new browser session), you will be prompted in the sidebar to enter your Google API Key. Paste your key into the input field. The application will validate it.

3.  **Database Initialization:**
    If the application detects that the database file (`people_say.db` by default, check `config.py`) doesn't exist or is empty, it will attempt to initialize it automatically using `database_init.py`. This might take a moment on the first run.

4.  **Start Searching:**
    Once the API key is validated and the database is ready, you can enter your questions into the main text area, select an analysis type, and click "✨ Search Insights".

## Architecture

The application follows a modular structure:

*   **`app.py` (Frontend & UI):**
    *   Built using Streamlit.
    *   Handles user input (query, API key, analysis type).
    *   Displays results (summary, sources, SQL query).
    *   Manages application flow and state (using `st.session_state`).
*   **`core_logic.py` (Orchestrator):**
    *   Contains the main `process_query` function.
    *   Coordinates the steps: LLM call for SQL generation -> Database query execution -> LLM call for summarization.
    *   Interfaces between the frontend (`app.py`) and the backend modules (`llm_inference.py`, database interaction).
*   **`llm_inference.py` (AI Interaction):** (Assumed based on `app.py` imports/calls)
    *   Handles all communication with the Google Generative AI API.
    *   Includes functions to configure the API client (`configure_genai`).
    *   Contains logic to generate SQL queries based on user input and schema.
    *   Contains logic to generate summaries based on retrieved data and user query/analysis type.
*   **`prompts.py` (LLM Prompts):**
    *   Stores the various prompt templates used for interacting with the LLM (e.g., for SQL generation, different summarization types).
*   **`database_init.py` (Database Setup):**
    *   Contains the logic to create the SQLite database (`people_say.db`) and populate it with data (likely from CSV or other source files - *ensure these source files are handled appropriately, e.g., via `.gitignore` if large/private*).
*   **`config.py` (Configuration):**
    *   Stores configuration variables like the database file path (`DB_PATH`).
*   **`people_say.db` (Database):**
    *   The SQLite database file containing the data from the "People Say" project.

## Configuration

*   **Google API Key:** Must be provided via the application's sidebar UI. It is *not* stored in configuration files or environment variables by default in this setup, enhancing security for local use.
*   **Database Path:** Defined in `config.py`.

## Data Source

This tool utilizes data from the [People Say](https://thepeoplesay.org/) project, developed by the Public Policy Lab and funded by The SCAN Foundation. It contains qualitative data about the experiences of older adults in the United States.

## Disclaimer

*   **AI Limitations:** The AI-generated SQL queries and summaries may sometimes be inaccurate or incomplete. Always critically evaluate the results and refer to the cited sources.
*   **API Key Security:** Your Google API key is only stored in the browser's session state for the duration of your session. It is not saved persistently by the application. Do not share your API key.
*   **Data Privacy:** Ensure compliance with any data privacy regulations or terms of use associated with the "People Say" dataset.
