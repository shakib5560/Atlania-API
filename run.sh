#!/bin/bash

# Navigate to the script's directory (backend root)
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run uvicorn from the backend root
echo "Starting Atlania Backend..."
uvicorn app.main:app --reload
