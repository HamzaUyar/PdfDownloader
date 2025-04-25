# Use an official Python slim image as a parent image
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry specific environment variables
    POETRY_VERSION=1.8.2 \
    # make poetry install packages to the virtual env in the project directory
    POETRY_VIRTUALENVS_IN_PROJECT=true \
     # do not ask any interactive question
    POETRY_NO_INTERACTION=1

# System dependencies (if any needed, e.g., for building certain packages)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only files necessary for dependency installation first to leverage Docker cache
COPY pyproject.toml poetry.lock* ./

# Install dependencies using Poetry
# --only main: Only install main dependencies (no dev dependencies)
# --no-root: Don't install the project itself as editable, done in the next step
RUN poetry install --only main --no-root

# Create the directory for downloads within the container
RUN mkdir -p /app/downloads

# Copy the application code into the container
COPY ./backend /app/backend
COPY ./frontend /app/frontend

# Expose the ports the apps run on
EXPOSE 8000
EXPOSE 8501

# Define the command to run the application using Uvicorn (will be overridden by docker-compose)
CMD ["poetry", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"] 