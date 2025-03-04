FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    git && \
    rm -rf /var/lib/apt/lists/*

# Clone the submodule to get the data/ directory
RUN git clone --recursive https://github.com/7azmi/ChatUTM-Data.git data

# Copy everything else
COPY . ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run main.py
CMD ["python", "main.py"]
