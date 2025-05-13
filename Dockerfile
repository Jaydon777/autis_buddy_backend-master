# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libopenblas-dev \
    libfreetype6 \
    libpng-dev \
    libjpeg-dev \
    zlib1g-dev \
    libsndfile1 \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all necessary files and directories
COPY api.py .
COPY config/ config/
COPY core/ core/
COPY output/ output/
COPY utils/ utils/
COPY visualization/ visualization/
COPY uploads/ uploads/
COPY data/ data/

# Expose the port FastAPI will run on
EXPOSE 8005

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8005"]