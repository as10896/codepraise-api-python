import asyncio


class RepoFile:
    BLAME_CMD = "git blame --line-porcelain"

    def __init__(self, filename: str):
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @property
    async def blame(self) -> str:
        if not hasattr(self, "_blame_output"):
            cmd = f"{self.BLAME_CMD} {self._filename}"
            process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            self._blame_output = stdout.decode()

        return self._blame_output
