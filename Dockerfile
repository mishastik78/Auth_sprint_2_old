FROM python:3.10.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

COPY src/. /usr/src/app

ENTRYPOINT /usr/local/bin/gunicorn wsgi_app:app -w 4 --bind 0.0.0.0:5000