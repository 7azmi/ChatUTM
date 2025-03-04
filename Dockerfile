# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Install git to handle submodules
RUN apt-get update && apt-get install -y git

# Initialize and update submodules
RUN git submodule init && git submodule update

# Set environment variables (if any)
# ENV PYTHONUNBUFFERED=1

# Run the command to start your application
CMD ["python", "embed_documents.py"]