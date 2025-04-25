# backend/api/endpoints/pdf_routes.py
from fastapi import APIRouter, Body, Depends
from typing import List, Union
from backend.api.models import (
    Guideline, InputPayload, CheckLinksResponse, DownloadPDFsResponse
)
from backend.services.pdf_service import pdf_service, PdfService

router = APIRouter()

# Dependency Injection could be used here for more complex scenarios,
# but direct import is fine for this simple case.
# async def get_pdf_service() -> PdfService:
#     return pdf_service

@router.post("/check-links", response_model=CheckLinksResponse, summary="Check PDF Link Accessibility")
async def check_links_endpoint(payload: Union[Guideline, List[Guideline], InputPayload] = Body(...)):
    """
    Accepts a JSON payload containing guidelines with PDF links, checks accessibility,
    and returns the status of each unique link.
    """
    # Convert single Guideline to InputPayload
    if isinstance(payload, Guideline):
        payload = InputPayload(data=[payload])
    # Convert list to InputPayload if needed
    elif isinstance(payload, list):
        payload = InputPayload(data=payload)
        
    results = await pdf_service.check_pdf_links(payload)
    return CheckLinksResponse(results=results)

@router.post("/download-pdfs", response_model=DownloadPDFsResponse, summary="Download Accessible PDFs")
async def download_pdfs_endpoint(payload: Union[Guideline, List[Guideline], InputPayload] = Body(...)):
    """
    Accepts a JSON payload containing guidelines with PDF links,
    attempts to download them, and returns the status.
    """
    # Convert single Guideline to InputPayload
    if isinstance(payload, Guideline):
        payload = InputPayload(data=[payload])
    # Convert list to InputPayload if needed
    elif isinstance(payload, list):
        payload = InputPayload(data=payload)
        
    results = await pdf_service.download_pdf_files(payload)
    return DownloadPDFsResponse(results=results) 