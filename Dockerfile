ARG BASE_IMAGE=python:3.11-slim-buster
FROM $BASE_IMAGE

WORKDIR /lru-cache-api

RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

COPY . .

CMD ["python", "-m", "app.main"]