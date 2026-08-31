FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by opencv, pymupdf, etc.
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Add FastAPI dependencies
RUN echo "fastapi==0.104.1" >> requirements.txt
RUN echo "uvicorn==0.24.0" >> requirements.txt
RUN echo "python-multipart==0.0.6" >> requirements.txt

# Remove conflicting/unnecessary windows/macos build packages from requirements if any
RUN sed -i '/cryptography/d' requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Expose port for Hugging Face Spaces (default 7860)
EXPOSE 7860

# Run the web server
CMD ["uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "7860"]
