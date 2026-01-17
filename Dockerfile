# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (if any are needed for psycopg2, etc.)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy project
COPY . .

# Expose port (documentary)
EXPOSE 8000

# Command to run the application
# We use shell form to allow variable expansion if needed, but array form is preferred for signal handling.
# However, many PAAS inject PORT env var, so we need to use it.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
