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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Page Configuration (Optional) ---
st.set_page_config(
    page_title="People Say AI Search",
    page_icon="🗣️", # Optional: Add a relevant emoji
    layout="wide" # Use wide layout for better display of results
)

# --- Application Title ---
st.title("🗣️ People Say AI Search Tool")
st.caption("Query the People Say database using natural language.")

# --- API Key Management in Sidebar ---
st.sidebar.header("API Key Configuration")

# Get the API key from session state if available, otherwise from config
if 'api_key' not in st.session_state:
    st.session_state.api_key = config.GOOGLE_API_KEY or ""

# Always show the API key input field
api_key = st.sidebar.text_input(
    "Enter your Google API Key:", 
    value=st.session_state.api_key,
    type="password",
    help="Required to use the AI functionality. Get a key from Google AI Studio."
)

# Process the API key if provided
if api_key:
    if api_key != st.session_state.api_key:
        # Update the session state and configuration
        st.session_state.api_key = api_key
        os.environ["GOOGLE_API_KEY"] = api_key
        config.GOOGLE_API_KEY = api_key
        
        # Reconfigure the genai client with the new API key
        import llm_inference
        if llm_inference.configure_genai():
            st.sidebar.success("✅ API Key configured successfully")
        else:
            st.sidebar.error("❌ Failed to configure API key. Please check if it's valid.")
else:
    st.sidebar.error("⚠️ Please enter a Google API Key to use this application")

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
    """
)
st.sidebar.warning(
    """
    **Note:**
    - AI-generated content may require verification.
    - You must provide a valid Google API Key in the field above.
    - The `peoplesay.db` file must be in the same directory.
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
button_disabled = not api_key  # Disable if no API key
if st.button("✨ Search Insights", disabled=button_disabled):
    if user_query:
        logging.info(f"Search button clicked with query: {user_query}")
        # Show a spinner while processing
        with st.spinner("🧠 Thinking... Generating SQL, querying DB, and summarizing..."):
            try:
                # Call the core logic function to handle the entire process
                summary, sources, sql_query = core_logic.process_query(
                    user_query,
                    template_key=selected_template
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

