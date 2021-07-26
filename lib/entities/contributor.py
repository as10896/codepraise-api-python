from typing import Optional
from pydantic import BaseModel, StrictStr


class Contributor(BaseModel):
    username: StrictStr
    email: Optional[StrictStr]
