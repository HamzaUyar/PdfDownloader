# backend/utils/file_utils.py
import os
from urllib.parse import urlparse
from pathlib import Path
import httpx
from backend.config import DOWNLOAD_DIR

def ensure_download_dir_exists():
    """Creates the download directory if it doesn't exist."""
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

def generate_filename_from_url(url: str) -> str:
    """Generates a safe filename from a URL."""
    try:
        parsed_url = urlparse(url)
        file_name = os.path.basename(parsed_url.path)
        if not file_name or file_name == '/':
            # Generate a fallback name using hash if path is empty/root
            # Use a safer hash if needed, but hash() is simple for this example
            safe_part = str(hash(url)).replace('-', '_') # Basic safety
            file_name = f"downloaded_{safe_part}.pdf"
        elif not file_name.lower().endswith('.pdf'):
             # Ensure it has a .pdf extension if it looks like a file
             if '.' in file_name: # Avoid adding .pdf to directory-like paths
                  file_name += ".pdf"
             else: # If no extension, assume PDF and add it
                  file_name += ".pdf"

        # Basic sanitization (replace potentially problematic characters)
        # A more robust library might be needed for production use cases
        file_name = file_name.replace('/', '_').replace('\\', '_').replace(':', '_')

        return file_name
    except Exception:
        # Fallback in case of unexpected URL parsing errors
        return f"downloaded_{str(hash(url)).replace('-', '_')}.pdf"

async def save_stream_to_file(response: httpx.Response, file_path: Path) -> None:
    """Asynchronously saves the content stream from an httpx response to a file.
    Note: Assumes response is already being managed by a context manager in the calling code.
    """
    # No longer using async with response here since it's already managed in _download_single_pdf
    response.raise_for_status() # Check status code before writing
    with open(file_path, "wb") as f:
        async for chunk in response.aiter_bytes():
            f.write(chunk) 