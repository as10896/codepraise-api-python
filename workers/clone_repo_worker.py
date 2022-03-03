from celery import Celery
from kombu.utils.url import safequote

from app.domain.summary.repositories import GitRepo
from config import get_settings

from .clone_monitor import CloneMonitor
from .job_reporter import JobReporter

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
    def clone_repo(request_json: str) -> None:
        job = JobReporter(request_json, config)
        gitrepo = GitRepo(job.repo, config)

        if gitrepo.exists_locally:
            return

        job.report(CloneMonitor.starting_percent)
        for line in gitrepo.clone(verbose=True):
            job.report(CloneMonitor.progress(line))

        # Keep sending finished status to any latecoming subscribers
        job.report_each_second(5, CloneMonitor.finished_percent)
