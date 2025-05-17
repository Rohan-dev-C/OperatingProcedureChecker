#!/bin/bash
set -e

echo "Loading environment variables from .env"
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "Starting FastAPI server..."
uvicorn src.webapp.main:app --host 0.0.0.0 --port 8000 --reload
