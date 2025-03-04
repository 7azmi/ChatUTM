FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    git && \
    rm -rf /var/lib/apt/lists/*

# Copy everything including the data/ directory
COPY . ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure chroma_data directory exists
RUN mkdir -p /app/chroma_data

# Set the default command to run main.py
CMD ["python", "main.py"]
