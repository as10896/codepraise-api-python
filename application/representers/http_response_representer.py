from typing import Any, Dict, ClassVar
from pydantic import BaseModel


class HttpResponseRepresenter(BaseModel):
    code: str
    message: Any

    _HTTP_CODE: ClassVar[Dict[str, int]] = {
        "ok": 200,
        "created": 201,
        "processing": 202,
        "cannot_process": 422,
        "not_found": 404,
        "bad_request": 400,
        "conflict": 409,
        "internal_error": 500,
    }

    @property
    def http_code(self) -> int:
        return self._HTTP_CODE[self.code]

    @property
    def http_message(self) -> Dict[str, Any]:
        return {self._msg_or_error: self.message}

    @property
    def _http_success(self) -> bool:
        return self.http_code < 300

    @property
    def _msg_or_error(self) -> str:
        return "message" if self._http_success else "error"
