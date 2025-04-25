from pathlib import Path

# Define the base directory for downloads within the container
# The actual path '/app/downloads' will be used in Docker.
# This setting could be made more complex (e.g., environment variables) if needed.
DOWNLOAD_DIR = Path("/app/downloads") 