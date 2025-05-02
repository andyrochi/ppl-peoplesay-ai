import streamlit as st
import os

st.set_page_config(page_title="About | People Say AI Search", page_icon="ℹ️", layout="wide")
st.sidebar.page_link("app.py", label="People Say AI Search", icon="🔎")
st.sidebar.page_link("pages/about.py", label="About", icon="ℹ️")
st.title("About People Say AI Search Tool")

about_md_path = os.path.join(os.path.dirname(__file__), "..", "docs", "about.md")
try:
    with open(about_md_path, "r") as f:
        st.markdown(f.read())
except FileNotFoundError:
    st.error("about.md not found in docs/.")

st.markdown("[⬅️ Back to Search](app.py)")