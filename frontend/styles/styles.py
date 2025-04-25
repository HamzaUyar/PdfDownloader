"""Styles for the PDF Downloader frontend."""

def get_css():
    """Returns the CSS styling for the application."""
    return """
    /* Theme-aware base styling */
    :root {
        --background-color: #f8f9fa;
        --card-background: white;
        --card-border: rgba(0, 0, 0, 0.1);
        --text-primary: #1e293b;
        --text-secondary: #334155;
        --accent-primary: #4361ee;
        --accent-hover: #3a56d4;
        --accent-secondary: #10b981;
        --accent-secondary-hover: #059669;
        --error-color: #ef4444;
        --shadow-color: rgba(0, 0, 0, 0.1);
        --input-border: #e2e8f0;
    }

    /* Dark theme overrides */
    [data-theme="dark"] {
        --background-color: #0e1117;
        --card-background: #1e1e1e;
        --card-border: rgba(255, 255, 255, 0.1);
        --text-primary: #e2e8f0;
        --text-secondary: #cbd5e1;
        --shadow-color: rgba(0, 0, 0, 0.3);
        --input-border: #2d3748;
    }

    /* Base styling */
    .stApp {
        background-color: var(--background-color);
    }
    
    /* Containers */
    .main-container, .result-container {
        background-color: var(--card-background);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px var(--shadow-color);
        margin-bottom: 0.75rem;
        border: 1px solid var(--card-border);
    }
    
    /* Hide empty containers */
    .stElementContainer:has(.main-container:empty),
    .stMarkdownContainer:has(.main-container:empty),
    .stMarkdown:has(.main-container:empty),
    .st-emotion-cache-seewz2:has(.main-container:empty),
    div:has(> .main-container:empty) {
        display: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: var(--accent-primary);
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: var(--accent-hover);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(67, 97, 238, 0.3);
    }
    
    .download-btn > button {
        background-color: var(--accent-secondary);
    }
    
    .download-btn > button:hover {
        background-color: var(--accent-secondary-hover);
        box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 5px;
        border: 1px solid var(--input-border);
        padding: 10px;
        transition: all 0.3s ease;
        background-color: var(--card-background);
        color: var(--text-primary);
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: var(--accent-primary);
        box-shadow: 0 0 0 2px rgba(67, 97, 238, 0.2);
    }
    
    /* Data display */
    .stDataFrame {
        border: none;
        border-radius: 10px;
        box-shadow: 0 2px 4px var(--shadow-color);
    }
    
    /* Typography */
    h1 {
        color: var(--text-primary);
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }
    
    h2, h3 {
        color: var(--text-secondary);
        font-weight: 600;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Stats cards */
    .stat-card {
        background-color: var(--card-background);
        padding: 0.75rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px var(--shadow-color);
        text-align: center;
        border: 1px solid var(--card-border);
        margin-bottom: 0.5rem;
    }
    
    .success-stat {
        border-left: 4px solid var(--accent-secondary);
    }
    
    .fail-stat {
        border-left: 4px solid var(--error-color);
    }
    
    /* Layout fixes */
    .sidebar .stMarkdown {
        line-height: 1.6;
        color: var(--text-primary);
    }
    
    /* Remove extra padding */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0 !important;
    }
    
    /* Remove extra spaces */
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }
    
    /* Reduce spacing in markdown */
    .stMarkdown {
        padding-bottom: 0 !important;
    }
    
    /* Additional fix for element-container with class kj6hex */
    .st-emotion-cache-kj6hex:has(.main-container:empty) {
        display: none !important;
    }
    
    /* Auto-detect theme and apply appropriate styles */
    @media (prefers-color-scheme: dark) {
        :root:not([data-theme="light"]) {
            --background-color: #0e1117;
            --card-background: #1e1e1e;
            --card-border: rgba(255, 255, 255, 0.1);
            --text-primary: #e2e8f0;
            --text-secondary: #cbd5e1;
            --shadow-color: rgba(0, 0, 0, 0.3);
            --input-border: #2d3748;
        }
    }

    /* Make sure Streamlit's default elements also work with theme */
    .stCodeBlock, .css-1q8dd3e {
        background-color: var(--card-background);
        border: 1px solid var(--card-border);
    }
    
    .st-emotion-cache-r421ms {
        border-color: var(--card-border);
    }
    
    .stAlert p {
        color: var(--text-secondary);
    }
    """

def apply_styles():
    """Apply all CSS styles to the Streamlit app."""
    import streamlit as st
    st.markdown(f"<style>{get_css()}</style>", unsafe_allow_html=True) 