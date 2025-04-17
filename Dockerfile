FROM python:3.12-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . /app

RUN adduser --disabled-password --no-create-home app
RUN chown -R app:app /app
USER app

RUN mkdir -p /app/staticfiles && chown -R app:app /app/staticfiles
RUN python manage.py collectstatic --no-input

EXPOSE 8000

