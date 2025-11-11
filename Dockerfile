FROM apache/superset:latest

USER root

# DB drivers
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev default-libmysqlclient-dev gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install drivers
RUN pip install --no-cache-dir psycopg2-binary pymysql mysqlclient

# Copy config
COPY superset_config.py /app/pythonpath/superset_config.py

USER superset
EXPOSE 8088

# FORCE PORT 8088
CMD ["gunicorn", "--bind", "0.0.0.0:8088", "--workers", "1", "--timeout", "300", "superset.app:create_app()"]
