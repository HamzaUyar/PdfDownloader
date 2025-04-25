# pdfdownloader/utils/http_client.py
import httpx
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, AsyncContextManager

# Global variable to hold the client instance
_client: Optional[httpx.AsyncClient] = None

@asynccontextmanager
async def lifespan_manager(app):
    """
    Manages the lifespan of the HTTP client.
    To be used with FastAPI's lifespan event handler.
    """
    global _client
    _client = httpx.AsyncClient(timeout=15.0, follow_redirects=True) # Default timeout
    print("HTTP Client started.")
    yield
    if _client:
        await _client.aclose()
        print("HTTP Client closed.")
    _client = None

def get_http_client() -> httpx.AsyncClient:
    """Provides access to the shared httpx client instance."""
    if _client is None:
        # This should ideally not happen if lifespan manager is used correctly
        raise RuntimeError("HTTP client is not initialized. Ensure lifespan manager is used.")
    return _client

async def perform_head_request(url: str) -> httpx.Response:
    """Performs an HTTP HEAD request using the shared client."""
    client = get_http_client()
    return await client.head(url)

def stream_download_request(url: str) -> AsyncContextManager[httpx.Response]:
    """Initiates an async streaming HTTP GET request for downloading."""
    client = get_http_client()
    # Use a longer timeout for potentially large downloads
    # The 'stream' context manager handles response closing
    return client.stream("GET", url, timeout=60.0) 