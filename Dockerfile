FROM apache/superset:latest

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    pkg-config \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY superset_config.py /app/pythonpath/superset_config.py

USER superset

EXPOSE 8088

CMD ["gunicorn", "-w", "1", "-k", "gevent", "--timeout", "300", "-b", "0.0.0.0:8088", "superset.app:create_app()"]




