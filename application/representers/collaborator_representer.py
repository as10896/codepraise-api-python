from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr


# Represents essential Collaborator information for API output
class CollaboratorRepresenter(BaseModel):
    origin_id: StrictInt
    username: StrictStr
    email: Optional[StrictStr]
