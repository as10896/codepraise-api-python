import requests

from config import Settings


class ProgressPublisher:
    def __init__(self, channel_id: str, config: Settings):
        self._channel_id = channel_id
        self._config = config

    def publish(self, message: str) -> None:
        print(f"Posting progress: {message}")
        response: requests.models.Response = requests.post(
            f"{self._config.API_URL}/progress/",
            json={
                "channel": f"{self._channel_id}",
                "data": message,
            },
        )
        print(response.status_code)

    def mock_publish(self, message: str) -> None:
        import requests_mock

        with requests_mock.Mocker() as mock:
            # For testing, just return a fake response from HTTP requests without making actual calls
            mock.post(f"{self._config.API_URL}/progress/", text="")
            self.publish(message)
