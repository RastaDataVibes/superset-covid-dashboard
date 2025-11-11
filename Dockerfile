# Use official Apache Superset image as base
FROM apache/superset:latest

USER root

# Install system dependencies for building Python packages and database drivers
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    gcc \
    python3-dev \
    pkg-config \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies first
COPY requirements.txt /app/requirements.txt

# Install all Python dependencies in Superset’s Python environment
RUN python3 -m pip install --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements.txt

# Copy Superset configuration
COPY superset_config.py /app/pythonpath/superset_config.py

# Fix permissions
RUN chown -R superset:superset /app

# Switch back to Superset user
USER superset

# Expose the Superset port
EXPOSE 8088

# Start Superset with Gunicorn using gevent worker
CMD ["gunicorn", "-w", "2", "-k", "gevent", "--timeout", "300", "-b", "0.0.0.0:8088", "superset.app:create_app()"]

