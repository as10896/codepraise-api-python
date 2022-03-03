from typing import Any, Dict, NamedTuple


class ServiceResult(NamedTuple):
    code: str
    message: Any

    def dict(self) -> Dict[str, Any]:
        return self._asdict()
