FROM apache/superset:latest

USER root

# FULL mysqlclient + pkg-config deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev \
    libmariadb-dev-compat \
    build-essential \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Bypass pkg-config for mysqlclient
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"

# INSTALL GEVENT + GUNICORN + DRIVERS FIRST (survives apache-superset override)
RUN pip install --no-cache-dir \
    gevent==24.2.1 \
    gunicorn[gevent]==23.0.0 \
    mysqlclient \
    psycopg2-binary \
    pymysql \
    faker

# Copy and FORCE reinstall Superset (keeps gevent)
COPY requirements.txt .
RUN pip install --no-cache-dir --force-reinstall --no-deps -r requirements.txt

# Config + monkey patch
COPY superset_config.py /app/pythonpath/superset_config.py
RUN sed -i '1i import gevent.monkey; gevent.monkey.patch_all()' /app/pythonpath/superset_config.py

USER superset
EXPOSE 8088

# PRODUCTION GEVENT CMD (free tier safe)
CMD ["gunicorn", "--bind", "0.0.0.0:8088", \
     "--workers", "2", \
     "--worker-class", "gevent", \
     "--worker-connections", "1000", \
     "--timeout", "300", \
     "--keep-alive", "5", \
     "superset.app:create_app()"]
