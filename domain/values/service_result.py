from typing import Any, NamedTuple, Dict


class ServiceResult(NamedTuple):
    code: str
    message: Any

    def dict(self) -> Dict[str, Any]:
        return self._asdict()
