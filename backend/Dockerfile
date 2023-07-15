FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl gcc build-essential libpq-dev libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -U pip \
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove gcc build-essential
COPY . /app
ENV PYTHONPATH "${PYTHONPATH}:/app"