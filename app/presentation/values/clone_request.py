from typing import Any, Iterator, NamedTuple, Tuple

from ...domain.entities import Repo


class CloneRequest(NamedTuple):
    repo: Repo
    id: int

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        # To make a CloneRequest object able to convert into a dictionary with `dict(obj)`
        # So later we could pass it into `BaseModel.parse_obj()`, turning into a CloneRequestRepresenter object
        for key in ["repo", "id"]:
            yield key, getattr(self, key)
