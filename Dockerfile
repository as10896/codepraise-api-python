# syntax=docker/dockerfile:1

FROM python:3.9-slim AS base

WORKDIR /app

# To install poetry, pyurl (for Amazon SQS conncection), and git (for cloning and blaming repos)
RUN apt-get update && \
    apt-get install -y curl gcc libcurl4-openssl-dev libssl-dev git

# To print directly to stdout instead of buffering output
ENV PYTHONUNBUFFERED=true

# Upgrade pip and install Poetry
RUN python -m pip install --upgrade pip && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry POETRY_PREVIEW=1 python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root

COPY . .

# ==================== production ====================

FROM base AS production

# To install psycopg2 (for PostgreSQL connection)
RUN apt-get install -y libpq-dev

RUN poetry install --no-root --with prod

EXPOSE 8000

CMD ["inv", "api.run.prod"]

# ==================== debug ====================

FROM base AS debug

RUN poetry install --no-root --with dev

EXPOSE 8000

CMD ["inv", "api.run.dev", "-h", "0.0.0.0"]


# ==================== test ====================

FROM base AS test

RUN poetry install --no-root --with test

CMD ["inv", "test"]
