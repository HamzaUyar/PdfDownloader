"""Module for displaying results in the PDF Downloader application."""
import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional

def display_results(results_data: Optional[Dict[str, Any]], results_placeholder):
    """
    Displays results or info/error messages in the placeholder.
    
    Args:
        results_data: The data returned from the API
        results_placeholder: The streamlit container to display results in
    """
    with results_placeholder.container():
        st.markdown('<div class="result-container" style="min-height: 1px;">', unsafe_allow_html=True)
        # First add the main header for results section with link anchor 
        st.markdown('<div id="results-section"></div><h2 style="margin-top: 0;">Results</h2>', unsafe_allow_html=True)
        
        if results_data and 'results' in results_data and results_data['results']:
            # Convert to DataFrame for better display
            df = pd.DataFrame(results_data['results'])
            
            # Count success/failure for different operations
            st.markdown("<h3 style='margin-top: 0.5rem;'>Summary</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            if 'status_code' in df.columns:  # Check links operation
                success_count = df[df['status'] == 'OK'].shape[0]
                failed_count = df[df['status'] != 'OK'].shape[0]
                
                with col1:
                    st.markdown(f"""
                    <div class="stat-card success-stat">
                        <h3 style="margin: 0;">✅ Accessible</h3>
                        <h2 style="margin: 0.5rem 0;">{success_count}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stat-card fail-stat">
                        <h3 style="margin: 0;">❌ Failed</h3>
                        <h2 style="margin: 0.5rem 0;">{failed_count}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    
            elif 'file_path' in df.columns:  # Download operation
                downloaded = df[df['status'] == 'DOWNLOADED'].shape[0]
                failed = df[df['status'] != 'DOWNLOADED'].shape[0]
                
                with col1:
                    st.markdown(f"""
                    <div class="stat-card success-stat">
                        <h3 style="margin: 0;">✅ Downloaded</h3>
                        <h2 style="margin: 0.5rem 0;">{downloaded}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stat-card fail-stat">
                        <h3 style="margin: 0;">❌ Failed</h3>
                        <h2 style="margin: 0.5rem 0;">{failed}</h2>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Add a separator before detailed results
            st.markdown("<hr style='margin: 1rem 0; border-color: var(--card-border);'>", unsafe_allow_html=True)
            
            st.markdown("<h3 style='margin-top: 0.5rem;'>Detailed Results</h3>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
        elif results_data:  # Backend responded, but no results list or empty
            st.info("No results returned or processed by the backend.")
        st.markdown('</div>', unsafe_allow_html=True) 