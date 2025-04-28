from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


class Project(BaseModel):
    id: UUID = uuid4()
    workspace_id: UUID
    name: str
    color: Optional[str] = None
    sort_order: int = 0
    is_archived: bool = False
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None