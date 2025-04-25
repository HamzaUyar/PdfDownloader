from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# --- Input Model ---
class InputPayload(BaseModel):
    id: int
    data: List[Dict[str, Any]]
    url: HttpUrl
    created_at: datetime

# --- Output Models ---
class LinkStatus(BaseModel):
    url: str
    status: str # "OK", "FAILED"
    status_code: Optional[int] = None
    error_message: Optional[str] = None

class DownloadStatus(BaseModel):
    url: str
    status: str # "DOWNLOADED", "FAILED_DOWNLOAD", "FAILED_CHECK"
    file_path: Optional[str] = None # Relative path inside container
    error_message: Optional[str] = None

# --- Response Wrappers ---
class CheckLinksResponse(BaseModel):
    results: List[LinkStatus]

class DownloadPDFsResponse(BaseModel):
    results: List[DownloadStatus] 