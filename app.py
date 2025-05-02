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
st.caption("Explore older adults' experiences using AI-driven search and traceable summaries.")

# --- Sidebar Configuration ---
st.sidebar.page_link("app.py", label="People Say AI Search", icon="🔎")
st.sidebar.page_link("pages/about.py", label="About", icon="ℹ️")

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

    **API Key:**
    You can get a Google API Key with the Generative Language API enabled from 
    [Google AI Studio](https://aistudio.google.com/app/apikey).

    """
)
st.sidebar.warning(
    """
    **Note:**
    - AI-generated content may require verification.
    - You must provide a valid Google API Key in the field above.
    """
)

st.markdown(
    """
    Welcome! This tool lets you ask questions about older adults' experiences and quickly surface insights from the [People Say qualitative dataset](https://thepeoplesay.org/data/explore?search=&filters=%5B%5D) using AI.
    """
)

st.page_link("pages/about.py", label="Learn more about this tool and its design philosophy", icon="ℹ️")

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

                # Create a two-column layout
                col1, col2 = st.columns([3, 2])  # Adjust ratio as needed (3:2 here)

                # Left column: Summary
                with col1:
                    st.markdown("**AI Generated Summary:**")
                    if summary:
                        st.markdown(summary)
                    else:
                        st.error("Could not retrieve or generate a summary.")

                    # SQL query at the bottom of left column
                    st.divider()
                    st.markdown("**Generated Database Query:**")
                    if sql_query:
                        st.code(sql_query, language="sql")
                    else:
                        st.caption("SQL query could not be generated.")

                # Right column: Citations
                with col2:
                    st.markdown("**Cited Sources:**")
                    if sources:
                        for i, source in enumerate(sources):
                            source_id = source.get('data_unit_title', f'Source {i+1}')
                            participant = source.get('participant_name', 'N/A')
                            excerpt_preview = source.get('data_unit', '')[:50] + '...'

                            with st.expander(f"**[{source_id}]**"):
                                # Participant info section
                                st.markdown(f"**Participant:** {participant}")
                                
                                # Demographic info
                                demo_cols = st.columns(2)
                                with demo_cols[0]:
                                    st.caption(f"Age: {source.get('age', 'N/A')}")
                                    st.caption(f"Gender: {source.get('gender', 'N/A')}")
                                    st.caption(f"Race/Ethnicity: {source.get('participant_race_ethnicity', 'N/A')}")
                                    st.caption(f"Language: {source.get('language', 'N/A')}")
                                
                                with demo_cols[1]:
                                    st.caption(f"State: {source.get('state', 'N/A')}")
                                    st.caption(f"Location Type: {source.get('location_type', 'N/A')}")
                                    st.caption(f"Income Range: {source.get('income_range_fpl', 'N/A')}")
                                    st.caption(f"Insurance: {source.get('participant_insurance', 'N/A')}")
                                
                                # Excerpt section
                                st.markdown("**Excerpt:**")
                                st.markdown(f"{source.get('data_unit', 'N/A')}")
                                
                                # Additional data (if available)
                                if 'relevant_subtopics' in source:
                                    st.caption(f"Subtopics: {source.get('relevant_subtopics', 'N/A')}")
                                
                                # Add link if available
                                if 'profile_picture_url' in source and source['profile_picture_url']:
                                    st.markdown(f"[View Profile]({source['profile_picture_url']})")
                    
                    elif summary and "No data found" not in summary and "Error:" not in summary:
                        st.info("Summary generated, but source details are unavailable.")
                    else:
                        st.info("No sources to display.")

            except Exception as e:
                # Catch any unexpected errors during the process
                logging.error(f"An unexpected error occurred in the Streamlit app: {e}", exc_info=True)
                st.error(f"An unexpected error occurred: {e}")

    else:
        # If the search button is clicked with no query
        st.warning("Please enter a question before searching.")
        logging.warning("Search button clicked without a user query.")

# with tabs[1]:
#     about_path = os.path.join(os.path.dirname(__file__), "docs", "about.md")
#     try:
#         with open(about_path, "r") as f:
#             st.markdown(f.read())
#     except FileNotFoundError:
#         st.error("about.md not found. Please add documentation in the docs/ folder.")

