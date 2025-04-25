"""Tests for API client functionality."""
import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime

from frontend.api_client import _prepare_payload

class TestApiClient(unittest.TestCase):
    """Test cases for the API client module."""

    def test_prepare_payload_valid_json_array(self):
        """Test payload preparation with valid JSON array."""
        test_url = "https://example.com"
        test_data = '[{"pdf_link": "https://example.com/doc1.pdf"}, {"pdf_link": "https://example.com/doc2.pdf"}]'
        
        with patch('frontend.api_client.datetime') as mock_datetime:
            mock_datetime.now.return_value.isoformat.return_value = "2023-01-01T00:00:00"
            
            payload = _prepare_payload(test_url, test_data)
            
            self.assertIsNotNone(payload)
            self.assertEqual(payload["url"], test_url)
            self.assertEqual(len(payload["data"]), 2)
            self.assertEqual(payload["data"][0]["pdf_link"], "https://example.com/doc1.pdf")
            self.assertEqual(payload["created_at"], "2023-01-01T00:00:00")

    def test_prepare_payload_valid_json_object(self):
        """Test payload preparation with valid JSON object."""
        test_url = "https://example.com"
        test_data = '{"pdf_link": "https://example.com/doc1.pdf"}'
        
        with patch('frontend.api_client.datetime') as mock_datetime:
            mock_datetime.now.return_value.isoformat.return_value = "2023-01-01T00:00:00"
            
            payload = _prepare_payload(test_url, test_data)
            
            self.assertIsNotNone(payload)
            self.assertEqual(payload["url"], test_url)
            self.assertEqual(len(payload["data"]), 1)
            self.assertEqual(payload["data"][0]["pdf_link"], "https://example.com/doc1.pdf")

    def test_prepare_payload_invalid_json(self):
        """Test payload preparation with invalid JSON."""
        test_url = "https://example.com"
        test_data = 'This is not JSON'
        
        with patch('frontend.api_client.st') as mock_st:
            payload = _prepare_payload(test_url, test_data)
            self.assertIsNone(payload)
            mock_st.error.assert_called()

if __name__ == '__main__':
    unittest.main() 