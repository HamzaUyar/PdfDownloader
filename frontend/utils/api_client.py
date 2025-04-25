"""API client for the backend."""
import json
import requests
import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional, List

from frontend import config

def _prepare_payload(data_str: str) -> Optional[Dict[str, Any]]:
    """
    Prepare the API payload from user inputs.
    
    Args:
        data_str: JSON string of data containing PDF links
        
    Returns:
        Dict payload or None if validation fails
    """
    try:
        # Try to parse the input data as JSON
        if data_str.strip().startswith('['):
            # It's a JSON array, try to parse
            data_list = json.loads(data_str)
            if not isinstance(data_list, list):
                st.error("Input data must be a JSON array.")
                return None
        else:
            # Try to handle as a single object
            try:
                single_item = json.loads(data_str)
                if isinstance(single_item, dict):
                    data_list = [single_item]
                else:
                    st.error("Input data must be a JSON array or object.")
                    return None
            except json.JSONDecodeError:
                st.error("Invalid JSON format. Please check your input data.")
                return None
        
        # Prepare the payload
        payload = {
            "id": 1,  # Default ID
            "data": data_list,
            "created_at": datetime.now().isoformat()
        }
        return payload
    
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON data: {e}")
        return None
    except Exception as e:
        st.error(f"Error preparing payload: {e}")
        return None

def _make_api_request(endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Make an API request to the backend.
    
    Args:
        endpoint: API endpoint URL
        payload: Request payload
        
    Returns:
        Response data or None on error
    """
    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30  # 30 second timeout
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    
    except requests.RequestException as e:
        st.error(f"Connection error: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

def check_links_api(data_str: str) -> Optional[Dict[str, Any]]:
    """
    Check PDF links API call.
    
    Args:
        data_str: JSON string of data containing PDF links
        
    Returns:
        API response or None on error
    """
    with st.spinner("Checking PDF links..."):
        payload = _prepare_payload(data_str)
        if payload:
            return _make_api_request(config.CHECK_LINKS_ENDPOINT, payload)
    return None

def download_pdfs_api(data_str: str) -> Optional[Dict[str, Any]]:
    """
    Download PDFs API call.
    
    Args:
        data_str: JSON string of data containing PDF links
        
    Returns:
        API response or None on error
    """
    with st.spinner("Downloading PDFs..."):
        payload = _prepare_payload(data_str)
        if payload:
            return _make_api_request(config.DOWNLOAD_PDFS_ENDPOINT, payload)
    return None 