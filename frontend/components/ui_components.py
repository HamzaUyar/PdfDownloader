"""UI components for the PDF Downloader application."""
import streamlit as st

def setup_page_config():
    """Configure the Streamlit page settings."""
    # Force dark theme 
    st.set_page_config(
        page_title="PDF Downloader", 
        page_icon="📄", 
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': "PDF Downloader - Dark Mode Edition"
        }
    )
    
    # Force dark mode by hiding theme options and adding dark theme CSS
    st.markdown("""
    <style>
    /* Force dark theme */
    [data-testid="stSidebar"] [data-testid="stToolbar"] {
        visibility: hidden;
    }
    
    /* Hide theme toggle in settings menu */
    section[data-testid="stSidebar"] div[data-testid="stToolbar"] button:nth-child(3),
    section[data-testid="stSidebar"] div[data-testid="stToolbar"] button:nth-child(2) {
        display: none;
    }
    
    /* Force dark theme colors */
    :root {
        --background-color: #0e1117;
        --card-background: #1e1e1e;
        --card-border: rgba(255, 255, 255, 0.1);
        --text-primary: #e2e8f0;
        --text-secondary: #cbd5e1;
        --shadow-color: rgba(0, 0, 0, 0.3);
        --input-border: #2d3748;
    }
    
    /* Override streamlit's theme settings */
    body, .stApp {
        background-color: var(--background-color) !important;
        color: var(--text-primary) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def setup_sidebar():
    """Setup the sidebar with application information."""
    with st.sidebar:
        st.markdown("""
        # 📄 PDF Downloader
        
        This application allows you to check PDF links and download them.
        """)
        
        st.markdown("## How to use")
        st.markdown("""
        1. Enter JSON data containing PDF links
        2. Click 'Check Links' to verify accessibility
        3. Click 'Download PDFs' to save the accessible PDFs
        """)
        
        st.markdown("## Sample JSON Data")
        st.code('''[
  {"pdf_link": "https://example.com/doc1.pdf"},
  {"pdf_link": "https://example.com/doc2.pdf"}
]''')

def render_header():
    """Render the application header."""
    st.markdown("<h1 style='text-align: center;'>📄 PDF Link Checker & Downloader</h1>", 
                unsafe_allow_html=True)

def render_input_section():
    """Render the input section of the application."""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown("### Enter your PDF links data")
    st.markdown("Provide JSON data containing PDF links to check accessibility or download.")

    # Input fields
    input_data = st.text_area(
        "JSON Data",
        height=150,
        placeholder='[{"pdf_link": "https://example.com/doc1.pdf"}, {"pdf_link": "https://example.com/doc2.pdf"}]'
    )

    # Action buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        check_button = st.button("🔍 Check Link Accessibility")
    with col_btn2:
        download_button = st.button("💾 Download PDFs", type="primary", use_container_width=True)
        st.markdown('<style>.element-container:has(.download-btn) button {background-color: var(--accent-secondary);}</style>', 
                    unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    return input_data, check_button, download_button 