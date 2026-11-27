# ==============================================================================
# GuardianNodes RoadSoS - Production Container
# ==============================================================================

FROM python:3.11-slim-bookworm

# Set environment variables for non-interactive and unbuffered execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# Install minimal system dependencies (curl for container healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user for security
RUN groupadd -r appuser && useradd -r -g appuser -m -d /home/appuser appuser

# Copy dependency requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application source code
COPY . .

# Set directory permissions for unprivileged user
RUN chown -R appuser:appuser /app

USER appuser

# Expose Streamlit default port
EXPOSE 8501

# Container healthcheck monitoring Streamlit core endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
