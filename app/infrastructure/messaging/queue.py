import time

import boto3

from config import Settings


# Queue wrapper for AWS SQS
class Queue:

    GROUP_ID = "codepraise_api_python"

    def __init__(self, queue_name: str, config: Settings):
        sqs = boto3.resource(
            "sqs",
            region_name=config.AWS_REGION,
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        )
        self._queue = sqs.get_queue_by_name(QueueName=queue_name)

    def send(self, message: str) -> None:
        """
        Sends message to queue

        To send messages to FIFO queue, you must provide the `MessageGroupId` for your messages explicitly.
        Ref: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html
        """
        unique = str(hash(message)) + str(hash(time.time()))
        self._queue.send_message(
            MessageBody=message,
            MessageGroupId=self.GROUP_ID,
            MessageDeduplicationId=unique,
        )
