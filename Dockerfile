FROM python:3.9.23-slim-bullseye

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        vim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Copy the requirements file
COPY requirements.txt .

# Install Python requirements
RUN pip install --break-system-packages -r requirements.txt