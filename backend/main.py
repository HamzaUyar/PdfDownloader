# backend/main.py
from fastapi import FastAPI
from backend.api.endpoints import pdf_routes
from backend.utils.http_client import lifespan_manager

# Create FastAPI app instance with lifespan management for the HTTP client
app = FastAPI(
    title="PdfDownloader API",
    description="Check and download PDF links.",
    version="0.1.0",
    lifespan=lifespan_manager # Register lifespan context manager
)

# Include the API router
app.include_router(pdf_routes.router, prefix="/api/v1") # Add a version prefix

@app.get("/", summary="Health Check")
async def read_root():
    """Basic health check endpoint."""
    return {"status": "API is running"}

# Note: No direct business logic here, just app setup and routing. 