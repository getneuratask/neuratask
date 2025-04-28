from pydantic import BaseModel
from uuid import UUID, uuid4
from datetime import datetime


class Workspace(BaseModel):
    id: UUID = uuid4()
    owner_id: UUID
    name: str
    created_at: datetime = datetime.now()