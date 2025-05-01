# app.py
"""
Main Streamlit application file for the People Say AI Search tool.

Provides the user interface for entering queries and displays the results.
"""

import streamlit as st
import core_logic # The module orchestrating the backend logic
import logging # Use logging
import prompts
import os
import config
from database_init import initialize_database  # Import the initialization function

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Page Configuration (Optional) ---
st.set_page_config(
    page_title="People Say AI Search",
    page_icon="🗣️", # Optional: Add a relevant emoji
    layout="wide" # Use wide layout for better display of results
)

# Initialize the database if needed (add this before the page config)
if not os.path.exists(config.DB_PATH) or os.path.getsize(config.DB_PATH) == 0:
    with st.spinner("Initializing database... This may take a moment..."):
        success = initialize_database()
        if not success:
            st.error("Failed to initialize the database. Please check the logs for details.")
            st.stop()

# --- Application Title ---
st.title("🗣️ People Say AI Search Tool")
st.caption("Query the People Say database using natural language.")

# --- API Key Management in Sidebar ---
st.sidebar.header("API Key Configuration")

# Get the API key from session state if available, otherwise initialize empty
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""  # Don't read from config, start empty
    st.session_state.api_key_valid = False

# If we already have a valid API key, just show status and option to change
if st.session_state.get('api_key_valid', False):
    st.sidebar.success("✅ API Key configured successfully")
    
    # Add a button to allow changing the key if needed
    if st.sidebar.button("Change API Key"):
        st.session_state.show_api_input = True
    
    # Only show the field if explicitly requested
    if st.session_state.get('show_api_input', False):
        new_api_key = st.sidebar.text_input(
            "Enter new Google API Key:", 
            value="",
            type="password",
            help="Required to use the AI functionality. Get a key from Google AI Studio."
        )
        
        if new_api_key:
            # Only update session state, not env vars or config
            st.session_state.api_key = new_api_key
            
            import llm_inference
            # Pass API key directly to configure_genai
            st.session_state.api_key_valid = llm_inference.configure_genai(api_key=new_api_key)
            st.session_state.show_api_input = False  # Hide input again
            
            if st.session_state.api_key_valid:
                st.sidebar.success("✅ New API Key configured successfully")
            else:
                st.sidebar.error("❌ Failed to configure API key. Please check if it's valid.")
                # Keep showing the input field if validation failed
                st.session_state.show_api_input = True
else:
    # Always show the API key input field if we don't have a valid key
    api_key = st.sidebar.text_input(
        "Enter your Google API Key:", 
        value=st.session_state.api_key,
        type="password",
        help="Required to use the AI functionality. Get a key from Google AI Studio."
    )
    
    if api_key:
        if api_key != st.session_state.api_key or not st.session_state.get('api_key_valid', False):
            # Only update session state, not env vars or config
            st.session_state.api_key = api_key
            
            import llm_inference
            # Pass API key directly to configure_genai
            st.session_state.api_key_valid = llm_inference.configure_genai(api_key=api_key)
            
            if st.session_state.api_key_valid:
                st.sidebar.success("✅ API Key configured successfully")
            else:
                st.sidebar.error("❌ Failed to configure API key. Please check if it's valid.")
    else:
        st.session_state.api_key_valid = False
        st.sidebar.error("⚠️ Please enter a Google API Key to use this application")

# For debugging - display current validation state (can remove later)
# st.sidebar.text(f"API key valid: {st.session_state.get('api_key_valid', False)}")

# --- Sidebar Information ---
st.sidebar.info(
    """
    **About:**
    This tool uses AI (Google's Generative Models) to understand your questions,
    search the People Say database for relevant excerpts, and generate a
    summary with citations.

    **Database:**
    Based on the [People Say](https://thepeoplesay.org/) project by the
    Public Policy Lab, funded by The SCAN Foundation.

    **Security Note**: 
    Your API key is stored only in your current browser session.
    Each browser window uses its own API key, so you'll need to 
    enter it once per browser session.
    """
)
st.sidebar.warning(
    """
    **Note:**
    - AI-generated content may require verification.
    - You must provide a valid Google API Key in the field above.
    """
)

# --- Main Input Area ---
# default_query = "How do older adults from Tribal communities feel about their access to specialist care?"
default_query = "How do older asians feel about their access to health care?"
user_query = st.text_area( # Use text_area for potentially longer queries
    "Enter your question about older adults' experiences:",
    value=default_query,
    height=100
)

# --- Analysis Type Selection ---
st.subheader("Analysis Type")
selected_template = st.radio(
    "Select analysis approach:",
    options=list(prompts.SUMMARY_TEMPLATES.keys()),
    index=0,  # Default to the first option
    help="Choose the type of analysis to perform on the retrieved data."
)

# Description of the selected template type
template_descriptions = {
    "Thematic Analysis": "Identifies recurring patterns, concepts, and themes across participants.",
    "Narrative Analysis": "Focuses on storytelling elements and how participants construct their experiences.",
    "Demographic Comparison": "Compares experiences across different demographic groups.",
    "Policy Implications": "Extracts insights relevant to policy development and system improvements."
}

st.caption(template_descriptions.get(selected_template, ""))

# --- Search Button and Processing Logic ---
# Only enable the button if we have a VALID API key
button_disabled = not (st.session_state.api_key and st.session_state.get('api_key_valid', False))
if st.button("✨ Search Insights", disabled=button_disabled):
    if user_query:
        logging.info(f"Search button clicked with query: {user_query}")
        # Show a spinner while processing
        with st.spinner("🧠 Thinking... Generating SQL, querying DB, and summarizing..."):
            try:
                # Call the core logic function to handle the entire process
                summary, sources, sql_query = core_logic.process_query(
                    user_query,
                    template_key=selected_template,
                    api_key=st.session_state.api_key
                )

                # --- Display Results ---
                st.subheader("🔍 Search Results")

                # Display Generated Summary
                st.markdown("**AI Generated Summary:**")
                if summary:
                    # Use markdown for better formatting possibilities (like lists, bolding from LLM)
                    st.markdown(summary)
                else:
                    # Handle cases where summary is None or an error message
                    st.error("Could not retrieve or generate a summary.")

                st.divider() # Visual separator

                # Display Sources if available
                st.markdown("**Cited Sources:**")
                if sources:
                    # Iterate through the list of source dictionaries
                    for i, source in enumerate(sources):
                        # Use an expander for each source to keep the UI clean
                        # Use participant name and maybe first few words of excerpt in title
                        source_id = source.get('data_unit_title', f'Source {i+1}') # Fallback ID
                        participant = source.get('participant_name', 'N/A')
                        excerpt_preview = source.get('data_unit', '')[:75] + '...' # Preview

                        with st.expander(f"**[{source_id}]** - {participant} - *{excerpt_preview}*"):
                            st.caption(f"Participant: {participant}")
                            # Display the full excerpt (which is in data_unit)
                            st.markdown(f"**Excerpt:**\n{source.get('data_unit', 'N/A')}")

                            # Optional: Display other relevant fields from the source dictionary if needed
                            # e.g., st.caption(f"Age: {source.get('age', 'N/A')}")
                            # e.g., st.caption(f"State: {source.get('state', 'N/A')}")

                            # Add link if you have a URL field and selected it in SQL
                            # if 'url' in source and source['url']:
                            #    st.markdown(f"[Link to original context]({source['url']})", unsafe_allow_html=True)

                elif summary and "No data found" not in summary and "Error:" not in summary:
                     st.info("Summary generated, but source details are unavailable.")
                else:
                    st.info("No sources to display.") # If summary indicated no data or error

                st.divider()

                # Optional: Display the generated SQL for transparency/debugging
                st.markdown("**Generated Database Query:**")
                if sql_query:
                    st.code(sql_query, language="sql")
                else:
                    st.caption("SQL query could not be generated.")

            except Exception as e:
                # Catch any unexpected errors during the process
                logging.error(f"An unexpected error occurred in the Streamlit app: {e}", exc_info=True)
                st.error(f"An unexpected error occurred: {e}")

    else:
        # If the search button is clicked with no query
        st.warning("Please enter a question before searching.")
        logging.warning("Search button clicked without a user query.")

