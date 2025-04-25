"""Configuration for the frontend."""
import os

# Backend service connection
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")
API_BASE_URL = f"{BACKEND_URL}/api/v1"

# Endpoints
CHECK_LINKS_ENDPOINT = f"{API_BASE_URL}/check-links"
DOWNLOAD_PDFS_ENDPOINT = f"{API_BASE_URL}/download-pdfs" 