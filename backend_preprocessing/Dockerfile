# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y gcc

# Copy requirements and install dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY src/ .

# Set environment variables (if needed)
# ENV SOME_ENV_VAR=some_value

# Expose port if running an API server (optional)
# EXPOSE 8000

# Run your main entrypoint
CMD ["python", "-m", "api.main"]