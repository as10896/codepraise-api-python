import base64
import hashlib
import shlex
import subprocess
from typing import Iterator


# Manage remote Git repository for cloning
class RemoteRepo:
    def __init__(self, git_url: str):
        self._git_url = git_url

    @property
    def git_url(self) -> str:
        return self._git_url

    @property
    def unique_id(self) -> str:
        digest: bytes = hashlib.sha256(self._git_url.encode()).digest()
        return base64.urlsafe_b64encode(digest).decode()

    def local_clone(self, path: str) -> Iterator[str]:
        # Cloning into 'infrastructure/gitrepo/repostore/Now-T9kpggGS8Xd4IB_aU0b0zcM1VdYTPq_NRaMv2Bs='...
        # remote: Enumerating objects: 228, done.
        # remote: Total 228 (delta 0), reused 0 (delta 0), pack-reused 228
        # Receiving objects: 100% (228/228), 40.55 KiB | 703.00 KiB/s, done.
        # Resolving deltas: 100% (109/109), done.

        cmd = f"git clone --progress {self._git_url} {path}"
        with subprocess.Popen(
            shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ) as process:
            for line in process.stdout:
                yield line.decode()
