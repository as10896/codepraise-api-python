# Run with Docker
You can start all the services easily with Docker Compose.<br>
Before startup, make sure you have all the configurations set up as mentioned before.

For convenience, you can use a `.env` file with all the necessary variables configured as follows:

```shell
export GH_TOKEN=<github credentials>
export AWS_ACCESS_KEY_ID=<aws credentials>
export AWS_SECRET_ACCESS_KEY=<aws credentials>
export AWS_REGION=<aws credentials>
export CLONE_QUEUE=<aws sqs queue>
export REPORT_QUEUE=<aws sqs queue>
```

Then `source` the configuration file:

```shell
source .env
```

Notice that it is not recommended to `export` all these credentials directly in the shell since these will be logged into shell history if not inserted through secure input.<br>
Don't do that especially when you're using a shared device that might be accessed by multiple users.

## Development
Uvicorn + Celery + SQLite + In-memory Pub/Sub
```shell
docker compose up -d  # run services in the background
docker compose run --rm console  # run application console with database connected
docker compose down  # shut down all the services
```
After startup, you can visit <a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a> to see the interactive API documentation.

## Production
Gunicorn + Uvicorn + Celery + PostgreSQL + Redis Pub/Sub
```shell
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d  # run services in the background
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm console  # run application console with database connected
docker compose -f docker-compose.yml -f docker-compose.prod.yml down  # shut down all the services
docker compose -f docker-compose.yml -f docker-compose.prod.yml down -v  # shut down all the services and remove all the volumes
```
After startup, you can visit <a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a> to see the interactive API documentation.

## Testing
```shell
docker compose -f docker-compose.test.yml run --rm test  # run TDD tests
docker compose -f docker-compose.test.yml --profile bdd up -d  # run services for the usage of frontend BDD testing
docker compose -f docker-compose.test.yml --profile bdd down  # shut down all the services for BDD testing
```