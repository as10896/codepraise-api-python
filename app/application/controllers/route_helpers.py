from typing import Any, Dict, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from returns.pipeline import is_successful
from returns.result import Result

from ...presentation.representers import HttpResponseRepresenter
from ...presentation.responses import ApiResult

Representer = TypeVar("Representer", bound=BaseModel)


def represent_response(
    result: Result,
    representer_class: Representer,
    headers: Optional[Dict[str, str]] = None,
) -> ORJSONResponse:
    if is_successful(result):
        find_result: ApiResult = result.unwrap()

        http_response: HttpResponseRepresenter = HttpResponseRepresenter.parse_obj(
            find_result.dict()
        )

        # BaseModel.parse_obj() takes a dictionary, or an object that can use `dict(obj)` to
        #   convert into a dictionary (by defining `__iter__` method or something)
        # It can takes a BaseModel object directly, since BaseModel has its own `__iter__` method as well
        # We could do field filtering in this way, without using FastAPI's response_model parameter
        response_content: Representer = representer_class.parse_obj(find_result.message)
        response_content: Dict[str, Any] = jsonable_encoder(response_content)

        return ORJSONResponse(
            status_code=http_response.http_code,
            content=response_content,
            headers=headers,
        )

    else:
        find_result: ApiResult = result.failure()
        http_response: HttpResponseRepresenter = HttpResponseRepresenter.parse_obj(
            find_result.dict()
        )
        return ORJSONResponse(
            status_code=http_response.http_code, content=http_response.http_message
        )
