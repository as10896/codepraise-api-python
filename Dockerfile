# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /app

# Install dependencies necessary for pyurl installation (for Amazon SQS conncection), PostgreSQL connection, and git (for cloning and blaming repos)
RUN apt-get update && \
    apt-get install -y libcurl4-openssl-dev libssl-dev libpq-dev gcc git

# To print directly to stdout instead of buffering output
ENV PYTHONUNBUFFERED=true

# Install pipenv
RUN python -m pip install --upgrade pip && \
    pip install pipenv

COPY Pipfile Pipfile.lock ./

ARG INSTALL_DEV=false
RUN if [ ${INSTALL_DEV} = "true" ] ; then \
        pipenv install --dev --system --deploy --ignore-pipfile ; \
    else \
        pipenv install --system --deploy --ignore-pipfile ; \
    fi

COPY . .

EXPOSE 8000

CMD ["inv", "api.run.dev", "-h", "0.0.0.0"]
