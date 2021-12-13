import os
import boto3
from invoke import task

from config import get_settings


@task(
    help={
        "env": "Environment of the SQS queue to create. ['test'|'development'|'production'] [default: 'development']",
        "name": "The name of the new queue. It must end with the '.fifo' suffix since we use a FIFO queue here. If not specified, the name written in the `CLONE_QUEUE` secret file will be used.",
    }
)
def create(c, env="development", name=None):
    """
    Create SQS queue for Celery
    """

    os.environ["ENV"] = env
    config = get_settings()

    if not os.getenv("AWS_ACCESS_KEY_ID"):
        os.environ["AWS_ACCESS_KEY_ID"] = config.AWS_ACCESS_KEY_ID

    if not os.getenv("AWS_SECRET_ACCESS_KEY"):
        os.environ["AWS_SECRET_ACCESS_KEY"] = config.AWS_SECRET_ACCESS_KEY

    if not os.getenv("AWS_DEFAULT_REGION"):
        os.environ["AWS_DEFAULT_REGION"] = config.AWS_REGION

    if not name:
        name = config.CLONE_QUEUE

    sqs = boto3.resource("sqs")

    try:
        queue = sqs.create_queue(QueueName=name, Attributes={"FifoQueue": "true"})
        print("Queue created:")
        print(f"Name: {name}")
        print(f"Region: {config.AWS_REGION}")
        print(f"URL: {queue.url}")
        print(f"Environment: {config.environment}")
    except Exception as e:
        print(f"Error creating queue: {e}")


@task(
    help={
        "env": "Environment of the SQS queue to purge messages. ['test'|'development'|'production'] [default: 'development']",
        "url": "The URL of the queue to deletes messages. If not specified, the URL written in the `CLONE_QUEUE_URL` secret file will be used.",
    }
)
def purge(c, env="development", url=None):
    """
    Purge messages in SQS queue for Celery
    """
    os.environ["ENV"] = env
    config = get_settings()

    if not os.getenv("AWS_ACCESS_KEY_ID"):
        os.environ["AWS_ACCESS_KEY_ID"] = config.AWS_ACCESS_KEY_ID

    if not os.getenv("AWS_SECRET_ACCESS_KEY"):
        os.environ["AWS_SECRET_ACCESS_KEY"] = config.AWS_SECRET_ACCESS_KEY

    if not os.getenv("AWS_DEFAULT_REGION"):
        os.environ["AWS_DEFAULT_REGION"] = config.AWS_REGION

    if not url:
        url = config.CLONE_QUEUE_URL

    client = boto3.client("sqs")
    try:
        client.purge_queue(QueueUrl=url)
        print(f"Queue {url} purged")
    except Exception as e:
        print(f"Error purging queue: {e}")
