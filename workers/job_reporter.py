import time

from app.presentation.representers import CloneRequestRepresenter
from config import Settings

from .progress_publisher import ProgressPublisher


class JobReporter:
    def __init__(self, request_json: str, config: Settings):
        clone_request: CloneRequestRepresenter = CloneRequestRepresenter.parse_raw(
            request_json
        )

        self.repo = clone_request.repo
        self._config = config
        self._publisher = ProgressPublisher(clone_request.id, config)

    def report(self, msg: str) -> None:
        if self._config.environment == "test":
            self._publisher.mock_publish(msg)
        else:
            self._publisher.publish(msg)

    def report_each_second(self, seconds: int, msg: str) -> None:
        for _ in range(seconds):
            time.sleep(1)
            self.report(msg)
