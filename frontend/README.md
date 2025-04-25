# PDF Downloader Frontend

A Streamlit-based frontend for the PDF Downloader service that works with the existing FastAPI backend.

## Features

- Check PDF link accessibility
- Download accessible PDFs
- Simple and intuitive UI
- Real-time status updates

## Architecture

The frontend is built using:

- **Streamlit**: For the web interface
- **Poetry**: For Python dependency management
- **Docker**: For containerization and easy deployment

## Development

### Local Development

To run the frontend locally (outside Docker):

```bash
poetry install
poetry run streamlit run frontend/app.py
```

Make sure to set the `BACKEND_URL` environment variable to point to your backend service.

### Docker Deployment

The frontend is designed to be deployed alongside the backend using Docker Compose:

```bash
docker-compose up
```

This will start both the backend and frontend services.

## How to Use

1. Enter a source URL 
2. Enter JSON data containing PDF links in the format:
   ```json
   [
     {"pdf_link": "https://example.com/doc1.pdf"},
     {"pdf_link": "https://example.com/doc2.pdf"}
   ]
   ```
3. Click "Check Link Accessibility" to verify which links are accessible
4. Click "Download Accessible PDFs" to download the PDFs to the server

## API Integration

The frontend communicates with the backend API defined in the FastAPI service. It uses:

- `/api/v1/check-links` endpoint to check PDF link accessibility
- `/api/v1/download-pdfs` endpoint to download PDFs 