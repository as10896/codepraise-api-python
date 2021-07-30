from typing import Optional
from pydantic import BaseModel, StrictStr


# Domain entity object for git contributors
class Contributor(BaseModel):
    username: StrictStr
    email: Optional[StrictStr]
