ARG BASE_IMAGE=python:3.11-slim-buster
FROM $BASE_IMAGE

WORKDIR /lru-cache-api

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock .

RUN poetry config virtualenvs.create false && poetry install --only main --no-root

COPY . .

CMD ["python", "-m", "app.main"]