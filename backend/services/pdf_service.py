# backend/services/pdf_service.py
import asyncio
import httpx
from typing import List, Set
from backend.api.models import InputPayload, LinkStatus, DownloadStatus
from backend.utils import http_client, file_utils
from backend.config import DOWNLOAD_DIR

class PdfService:

    def extract_pdf_links(self, payload: InputPayload) -> Set[str]:
        """Extracts unique, valid-looking PDF links from the payload."""
        pdf_links = set()
        for item in payload.data:
            # If the item is a Guideline object, access the pdf_links attribute directly
            if hasattr(item, 'pdf_links') and isinstance(item.pdf_links, list):
                for link in item.pdf_links:
                    if link and isinstance(link, str) and link.lower().startswith(('http://', 'https://')):
                        pdf_links.add(link)
            # For backward compatibility with dictionary inputs
            elif isinstance(item, dict):
                # Check for pdf_links array
                if 'pdf_links' in item and isinstance(item['pdf_links'], list):
                    for link in item['pdf_links']:
                        if link and isinstance(link, str) and link.lower().startswith(('http://', 'https://')):
                            pdf_links.add(link)
                # Also check for pdf_link for backward compatibility
                elif 'pdf_link' in item:
                    link = item.get('pdf_link')
                    if link and isinstance(link, str) and link.lower().startswith(('http://', 'https://')):
                        pdf_links.add(link)
        return pdf_links

    async def check_pdf_links(self, payload: InputPayload) -> List[LinkStatus]:
        """Checks the status of PDF links extracted from the payload."""
        pdf_links = self.extract_pdf_links(payload)
        if not pdf_links:
            return []

        tasks = [self._check_single_link(url) for url in pdf_links]
        results = await asyncio.gather(*tasks)
        return results

    async def _check_single_link(self, url: str) -> LinkStatus:
        """Helper to check one link's status."""
        try:
            from backend.utils.file_utils import extract_pdf_url
            
            # Extract the actual PDF URL if this is a viewer URL
            pdf_url = extract_pdf_url(url)
            
            response = await http_client.perform_head_request(pdf_url)
            if response.status_code == 200:
                return LinkStatus(url=url, status="OK", status_code=response.status_code)
            else:
                return LinkStatus(url=url, status="FAILED", status_code=response.status_code, error_message=f"HTTP status code: {response.status_code}")
        except httpx.RequestError as exc:
            return LinkStatus(url=url, status="FAILED", error_message=f"Request error: {exc.__class__.__name__}")
        except Exception as exc:
            return LinkStatus(url=url, status="FAILED", error_message=f"Unexpected error: {str(exc)}")

    async def download_pdf_files(self, payload: InputPayload) -> List[DownloadStatus]:
        """Downloads PDF files from links extracted from the payload."""
        pdf_links = self.extract_pdf_links(payload)
        if not pdf_links:
            return []

        file_utils.ensure_download_dir_exists() # Ensure download dir exists

        tasks = [self._download_single_pdf(url) for url in pdf_links]
        results = await asyncio.gather(*tasks)
        return results

    async def _download_single_pdf(self, url: str) -> DownloadStatus:
        """Helper to download one PDF file."""
        try:
            from backend.utils.file_utils import extract_pdf_url
            
            # Extract the actual PDF URL if this is a viewer URL
            pdf_url = extract_pdf_url(url)
            
            # Optional pre-check with HEAD request
            head_response = await http_client.perform_head_request(pdf_url)
            head_response.raise_for_status() # Check if accessible before GET

            file_name = file_utils.generate_filename_from_url(url)
            save_path = DOWNLOAD_DIR / file_name

            # Perform streaming download
            async with http_client.stream_download_request(pdf_url) as response:
                 await file_utils.save_stream_to_file(response, save_path)
                 return DownloadStatus(url=url, status="DOWNLOADED", file_path=str(save_path))

        except httpx.HTTPStatusError as exc:
             # Error during HEAD check or GET stream opening
            return DownloadStatus(url=url, status="FAILED_CHECK", error_message=f"HTTP error: {exc.response.status_code} - {exc.__class__.__name__}")
        except httpx.RequestError as exc:
            # Network error during check or download
            return DownloadStatus(url=url, status="FAILED_CHECK", error_message=f"Request error: {exc.__class__.__name__}")
        except IOError as exc:
             # Error saving file
             return DownloadStatus(url=url, status="FAILED_DOWNLOAD", error_message=f"File writing error: {str(exc)}")
        except Exception as exc:
            # Other unexpected errors during the process
            # Add extra logging here too if needed
            print(f"Caught exception for {url}: {type(exc).__name__} - {str(exc)}")
            return DownloadStatus(url=url, status="FAILED_DOWNLOAD", error_message=f"Unexpected download error: {str(exc)}")

# Instantiate the service for use in the API layer
pdf_service = PdfService() 