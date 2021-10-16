import subprocess


class RepoFile:
    BLAME_CMD = "git blame --line-porcelain"

    def __init__(self, filename: str):
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @property
    def blame(self) -> str:
        if not hasattr(self, "_blame_output"):
            cmd = f"{self.BLAME_CMD} {self._filename}"
            process = subprocess.run(cmd.split(), capture_output=True, check=True)
            self._blame_output = process.stdout.decode()

        return self._blame_output
