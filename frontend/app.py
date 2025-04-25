"""Main Streamlit application for the PDF Downloader frontend."""
import streamlit as st
from typing import Dict, Any, Optional

# Import from modules using new directory structure
from frontend.config import *
from frontend.utils import check_links_api, download_pdfs_api
from frontend.styles import apply_styles
from frontend.components import (
    setup_page_config, 
    setup_sidebar, 
    render_header, 
    render_input_section,
    display_results
)

def main():
    """Main application entry point."""
    # Setup
    setup_page_config()
    apply_styles()
    
    # UI Components
    setup_sidebar()
    render_header()
    
    # Input Section
    input_data, check_button, download_button = render_input_section()
    
    # Results placeholder
    results_placeholder = st.empty()
    
    # --- Main Logic ---
    if check_button or download_button:
        # Clear previous results/errors before processing new request
        results_placeholder.empty()

        # Validate inputs
        if not input_data:
            st.warning("Please provide JSON data with PDF links.")
        else:
            # Call the appropriate API client function
            results = None
            if check_button:
                results = check_links_api(input_data)
            elif download_button:
                results = download_pdfs_api(input_data)

            # Display results (or errors shown by api_client)
            if results is not None:
                display_results(results, results_placeholder)

if __name__ == "__main__":
    main() 