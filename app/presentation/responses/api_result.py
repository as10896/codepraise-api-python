from typing import Any, Dict, NamedTuple


class ApiResult(NamedTuple):
    code: str
    message: Any

    def dict(self) -> Dict[str, Any]:
        return self._asdict()
