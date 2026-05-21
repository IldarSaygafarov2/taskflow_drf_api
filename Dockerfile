FROM python:3.14-slim

# Set environment variables to optimize Python for Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/


CMD ["gunicorn", "-c", "deploy/gunicorn_conf.py", "core.project.wsgi:application"]