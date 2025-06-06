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

# Copy the requirements file
COPY requirements.txt .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
COPY .env /app/.env

RUN echo "Conteúdo de /app/.env:" && cat /app/.env

# Set the environment variable for python
ENTRYPOINT ["python", "-m", "bot"]
