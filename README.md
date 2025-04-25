# PdfDownloader API

A simple backend service built with FastAPI and organized in a layered architecture. It processes JSON payloads to check the accessibility of PDF links and optionally downloads these PDFs. Dependencies are managed using Poetry.

## Features

* **/api/v1/check-links**: Checks PDF link accessibility.
* **/api/v1/download-pdfs**: Downloads accessible PDFs.

## Technologies Used

* Python 3.10+
* FastAPI
* Poetry (Dependency Management)
* Uvicorn
* HTTPX
* Pydantic
* Docker & Docker Compose

## Setup and Running

### Prerequisites

* Python 3.10+ and Poetry installed locally (https://python-poetry.org/docs/#installation)
* Docker Engine
* Docker Compose

### Steps

1.  **Clone Repository:**
    ```bash
    git clone <repository_url>
    cd PdfDownloader
    ```
2.  **(Local Development Setup - Optional):**
    ```bash
    poetry install # Installs dependencies including dev dependencies
    # To run locally (ensure downloads dir exists or is created by app):
    # mkdir downloads
    # poetry run uvicorn backend.main:app --reload
    ```
3.  **Create `downloads` Directory for Docker:**
    ```bash
    mkdir downloads
    ```
4.  **Run with Docker Compose (Recommended):**
    ```bash
    docker-compose up --build
    ```
    The API will be available at `http://localhost:8000`. Downloaded files will appear in the host's `./downloads` directory.

## API Usage

Endpoints are prefixed with `/api/v1`.

### 1. Check Links (`/api/v1/check-links`)

* **Method:** `POST`
* **URL:** `http://localhost:8000/api/v1/check-links`
* **Body (raw JSON):**
  ```json
  {
    "id": 123,
    "data": [
      {"pdf_link": "https://example.com/document1.pdf"},
      {"pdf_link": "https://example.com/document2.pdf"}
    ],
    "url": "https://example.com/source",
    "created_at": "2023-05-01T12:30:00Z"
  }
  ```
* **Response:**
  ```json
  {
    "results": [
      {
        "url": "https://example.com/document1.pdf",
        "status": "OK",
        "status_code": 200,
        "error_message": null
      },
      {
        "url": "https://example.com/document2.pdf",
        "status": "FAILED",
        "status_code": 404,
        "error_message": "HTTP status code: 404"
      }
    ]
  }
  ```

### 2. Download PDFs (`/api/v1/download-pdfs`)

* **Method:** `POST`
* **URL:** `http://localhost:8000/api/v1/download-pdfs`
* **Body (raw JSON):** Same as check-links endpoint
* **Response:**
  ```json
  {
    "results": [
      {
        "url": "https://example.com/document1.pdf",
        "status": "DOWNLOADED",
        "file_path": "/app/downloads/document1.pdf",
        "error_message": null
      },
      {
        "url": "https://example.com/document2.pdf",
        "status": "FAILED_CHECK",
        "file_path": null,
        "error_message": "HTTP error: 404 - HTTPStatusError"
      }
    ]
  }
  ```

## Stopping the Service

To stop the running service:

```bash
# If running with docker-compose:
docker-compose down

# If running locally:
# Ctrl+C in the terminal where uvicorn is running
``` 