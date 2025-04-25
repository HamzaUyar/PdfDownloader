# backend/utils/file_utils.py
import os
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import httpx
from backend.config import DOWNLOAD_DIR

def ensure_download_dir_exists():
    """Creates the download directory if it doesn't exist."""
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

def extract_pdf_url(url: str) -> str:
    """Extracts the actual PDF URL from viewer URLs.
    
    If the URL is a PDF viewer (like viewer.html?file=something.pdf), 
    this extracts the actual PDF file path.
    """
    parsed_url = urlparse(url)
    
    # Check if this is a PDF viewer URL
    if 'viewer.html' in parsed_url.path and 'file=' in url:
        # Extract the file parameter from the query string
        query_params = parse_qs(parsed_url.query)
        if 'file' in query_params and query_params['file']:
            pdf_path = query_params['file'][0]
            
            # Build the direct PDF URL
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            if pdf_path.startswith('/'):
                return f"{base_url}{pdf_path}"
            else:
                # Handle relative paths
                path_parts = parsed_url.path.split('/')
                # Remove the viewer.html part
                path_parts.pop()
                # Add the PDF path
                path_parts.append(pdf_path)
                return f"{base_url}{'/'.join(path_parts)}"
    
    # If not a viewer URL or extraction failed, return the original URL
    return url

def generate_filename_from_url(url: str) -> str:
    """Generates a safe filename from a URL."""
    try:
        # First, try to extract the actual PDF URL if this is a viewer URL
        pdf_url = extract_pdf_url(url)
        
        parsed_url = urlparse(pdf_url)
        file_name = os.path.basename(parsed_url.path)
        
        if not file_name or file_name == '/':
            # Generate a fallback name using hash if path is empty/root
            safe_part = str(hash(url)).replace('-', '_') # Basic safety
            file_name = f"downloaded_{safe_part}.pdf"
        elif not file_name.lower().endswith('.pdf'):
            # Ensure it has a .pdf extension if it looks like a file
            if '.' in file_name: # Avoid adding .pdf to directory-like paths
                file_name += ".pdf"
            else: # If no extension, assume PDF and add it
                file_name += ".pdf"

        # Basic sanitization (replace potentially problematic characters)
        file_name = file_name.replace('/', '_').replace('\\', '_').replace(':', '_')

        return file_name
    except Exception as e:
        print(f"Error generating filename from URL {url}: {e}")
        # Fallback in case of unexpected URL parsing errors
        return f"downloaded_{str(hash(url)).replace('-', '_')}.pdf"

async def save_stream_to_file(response: httpx.Response, file_path: Path) -> None:
    """Asynchronously saves the content stream from an httpx response to a file.
    Note: Assumes response is already being managed by a context manager in the calling code.
    """
    response.raise_for_status() # Check status code before writing
    with open(file_path, "wb") as f:
        async for chunk in response.aiter_bytes():
            f.write(chunk) 