from typing import Optional
from pydantic import BaseModel, StrictStr, StrictInt


# Domain entity object for git contributors
class Collaborator(BaseModel):
    id: Optional[int]
    origin_id: StrictInt
    username: StrictStr
    email: Optional[StrictStr]

    class Config:
        orm_mode = True
