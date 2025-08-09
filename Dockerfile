FROM apache/superset:latest

USER root
RUN pip install --no-cache-dir -r /app/requirements.txt
USER superset

EXPOSE 8088
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8088", "superset.app:create_app()"]

