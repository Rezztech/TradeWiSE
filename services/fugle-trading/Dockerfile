FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN --mount=type=cache,target=/root/.cache \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY docker-entrypoint.sh /
COPY src/ /app/

CMD ["/docker-entrypoint.sh"]
