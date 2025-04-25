"""Main Streamlit application for the PDF Downloader frontend."""
import streamlit as st
import os
from typing import Dict, Any, Optional
import pandas as pd

# Import from modules
from frontend import config
from frontend import api_client

# --- Styling ---
st.set_page_config(page_title="PDF Downloader", page_icon="📄", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .stTextArea>div>div>textarea {
        border-radius: 5px;
    }
    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    h1, h2, h3 {
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- Result Display Function ---
# Define placeholder early so display_results can access it
results_placeholder = st.empty()

def display_results(results_data: Optional[Dict[str, Any]]):
    """Displays results or info/error messages in the placeholder."""
    with results_placeholder.container():
        if results_data and 'results' in results_data and results_data['results']:
            # Convert to DataFrame for better display
            df = pd.DataFrame(results_data['results'])
            
            # Count success/failure for different operations
            if 'status_code' in df.columns:  # Check links operation
                success_count = df[df['status'] == 'OK'].shape[0]
                failed_count = df[df['status'] != 'OK'].shape[0]
                st.success(f"✅ Accessible: {success_count} | ❌ Failed: {failed_count}")
            elif 'file_path' in df.columns:  # Download operation
                downloaded = df[df['status'] == 'DOWNLOADED'].shape[0]
                failed = df[df['status'] != 'DOWNLOADED'].shape[0]
                st.success(f"✅ Downloaded: {downloaded} | ❌ Failed: {failed}")
            
            st.subheader("Results")
            st.dataframe(df)
        elif results_data:  # Backend responded, but no results list or empty
            st.info("No results returned or processed by the backend.")

# --- Sidebar with app info ---
with st.sidebar:
    st.header("About")
    st.info("This application allows you to check PDF links and download them.")
    st.markdown("**How to use:**")
    st.markdown("1. Enter a source URL")
    st.markdown("2. Enter JSON data containing PDF links")
    st.markdown("3. Click 'Check Links' to verify accessibility")
    st.markdown("4. Click 'Download PDFs' to save the accessible PDFs")
    
    st.markdown("---")
    st.markdown("**Sample JSON Data:**")
    st.code('''[
  {"pdf_link": "https://example.com/doc1.pdf"},
  {"pdf_link": "https://example.com/doc2.pdf"}
]''')

# --- Main UI ---
st.title("📄 PDF Link Checker & Downloader")

st.markdown("Enter data containing PDF links and a source URL to check accessibility or download.")

# Input fields
col1, col2 = st.columns(2)
with col1:
    url_input = st.text_input("Source URL", "https://example.com")

with col2:
    # Use text area for potentially large JSON input
    input_data_input = st.text_area(
        "Input Data (JSON format)",
        height=150,
        placeholder='[{"pdf_link": "https://example.com/doc1.pdf"}, {"pdf_link": "https://example.com/doc2.pdf"}]'
    )

# Action buttons
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    check_button = st.button("Check Link Accessibility")
with col_btn2:
    download_button = st.button("Download Accessible PDFs")

# --- Main Logic ---
if check_button or download_button:
    # Clear previous results/errors before processing new request
    results_placeholder.empty()

    # Validate inputs
    if not url_input or not input_data_input:
        st.warning("Please provide both Source URL and Input Data.")
    else:
        # Call the appropriate API client function
        results = None
        if check_button:
            results = api_client.check_links_api(url_input, input_data_input)
        elif download_button:
            results = api_client.download_pdfs_api(url_input, input_data_input)

        # Display results (or errors shown by api_client)
        if results is not None:
            display_results(results) 