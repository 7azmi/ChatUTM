# Use an official Python image as the base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the main repository files to the container
COPY . .

# Manually clone the submodule since Railway does not include .git
RUN rm -rf data && \
    git clone --recursive https://github.com/7azmi/ChatUTM-Data.git data

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port if your app runs on a specific port (optional)
EXPOSE 8000  # Change this if your app runs on a different port

# Start the application
CMD ["python", "main.py"]
FROM ubuntu:latest
LABEL authors="humadi"

ENTRYPOINT ["top", "-b"]