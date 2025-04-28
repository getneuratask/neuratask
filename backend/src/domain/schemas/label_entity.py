from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4


class Label(BaseModel):
    id: UUID = uuid4()
    workspace_id: UUID
    name: str
    color: Optional[str] = None