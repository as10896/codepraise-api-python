from celery import Celery
from kombu.utils.url import safequote

from application.representers import RepoRepresenter
from config import get_settings
from domain.mappers.git_mappers import GitRepo

config = get_settings()

aws_access_key = safequote(config.AWS_ACCESS_KEY_ID)
aws_secret_key = safequote(config.AWS_SECRET_ACCESS_KEY)

celery = Celery("worker", broker=f"sqs://{aws_access_key}:{aws_secret_key}@")

celery.conf.task_default_queue = config.CLONE_QUEUE
celery.conf.broker_transport_options = {
    "region": config.AWS_REGION,
}


# Celery worker class to clone repos in parallel
class CloneRepoWorker:
    @staticmethod
    @celery.task(acks_late=True)
    def clone_repo(worker_request: str):
        request: RepoRepresenter = RepoRepresenter.parse_raw(worker_request)
        print(f"REQUEST: {request}")
        gitrepo = GitRepo(request)
        print(f"EXISTS: {gitrepo.exists_locally}")
        if gitrepo.exists_locally:
            return
        gitrepo.clone()
        print(f"REQUEST: #{request}")
        print(f"EXISTS: #{gitrepo.exists_locally}")
