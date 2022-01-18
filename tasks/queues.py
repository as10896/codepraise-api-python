import os

import boto3
from invoke import task

from config import get_settings


@task(
    help={
        "env": "Environment of the SQS queue to create. ['test'|'development'|'production'] [default: 'development']"
    }
)
def create(c, env="development"):
    """
    Create SQS queue for Celery
    """
    def _create_queue(sqs, queue_name, config):
        try:
            queue = sqs.create_queue(QueueName=queue_name, Attributes={"FifoQueue": "true"})
            print("Queue created:")
            print(f"Name: {queue_name}")
            print(f"Region: {config.AWS_REGION}")
            print(f"URL: {queue.url}")
            print(f"Environment: {config.environment}")
        except Exception as e:
            print(f"Error creating queue: {e}")

    os.environ["ENV"] = env
    config = get_settings()

    sqs = boto3.resource(
        "sqs",
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    if config.environment == "test":
        _create_queue(sqs, config.CLONE_QUEUE, config)

    elif config.environment in ["development", "production"]:
        for queue_name in [config.CLONE_QUEUE, config.REPORT_QUEUE]:
            _create_queue(sqs, queue_name, config)


@task(
    help={
        "env": "Environment of the SQS queue to purge messages. ['test'|'development'|'production'] [default: 'development']"
    }
)
def purge(c, env="development"):
    """
    Purge messages in SQS queue for Celery
    """
    def _purge_queue(sqs, queue_name):
        try:
            queue = sqs.get_queue_by_name(QueueName=queue_name)
            queue.purge()
            print(f"Queue {queue_name} purged")
        except Exception as e:
            print(f"Error purging queue: {e}")

    os.environ["ENV"] = env
    config = get_settings()

    sqs = boto3.resource(
        "sqs",
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )
    
    if config.environment == "test":
        _purge_queue(sqs, config.CLONE_QUEUE)

    elif config.environment in ["development", "production"]:
        for queue_name in [config.CLONE_QUEUE, config.REPORT_QUEUE]:
            _purge_queue(sqs, queue_name)
