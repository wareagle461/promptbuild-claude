FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY prompt_generator.py .
COPY web_ui.py .
COPY example_batch.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_HOST=http://host.docker.internal:11434

# Create a non-root user
RUN useradd -m -u 1000 promptuser && \
    chown -R promptuser:promptuser /app

USER promptuser

# Default command (interactive mode)
CMD ["python", "prompt_generator.py"]
