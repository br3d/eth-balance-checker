FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including build tools for compilation
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt main.py config.json healthcheck.py prometheus_metrics.py /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Clean up build dependencies to reduce image size
RUN apt-get purge -y gcc python3-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/ || exit 1

CMD ["python", "main.py"]
