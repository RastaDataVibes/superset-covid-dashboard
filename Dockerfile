# Use the official Superset image as base
FROM apache/superset:latest

# we need root temporarily to install packages
USER root

# copy requirements into the image so pip can read them during build
COPY requirements.txt /app/requirements.txt

# install any extra Python packages listed in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy a custom superset config if you have one (optional)
# change path if your config is elsewhere
COPY superset_config.py /app/pythonpath/superset_config.py

# switch back to the superset user for safety
USER superset

# expose Superset port
EXPOSE 8088

# start Superset with gunicorn
CMD ["gunicorn", "-w", "4", "-k", "gevent", "--timeout", "300", "superset.app:create_app()", "-b", "0.0.0.0:8088"]


