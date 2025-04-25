from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# --- Guideline Model ---
class Guideline(BaseModel):
    id: int
    url: str
    domain: str
    breadcrumbs_japanese: Optional[str] = None
    breadcrumbs_english: Optional[str] = None
    title_japanese: Optional[str] = None
    title_english: Optional[str] = None
    publish_date: Optional[str] = None
    publish_year: Optional[int] = None
    publisher_japanese: Optional[str] = None
    publisher_english: Optional[str] = None
    pdf_links: List[str] = []
    created_at: Optional[datetime] = None

# --- Input Model ---
class InputPayload(BaseModel):
    data: List[Guideline]
    
    class Config:
        # Allow model to be initialized directly from a list of guidelines
        @classmethod
        def get_validators(cls):
            yield cls.validate
            
        @classmethod
        def validate(cls, v):
            if isinstance(v, list):
                return cls(data=v)
            return v

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