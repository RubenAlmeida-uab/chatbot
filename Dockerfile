FROM python:3.9.23-slim-bullseye

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        vim && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for python
ENTRYPOINT ["python", "bot.py"]
