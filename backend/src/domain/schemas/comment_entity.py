from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


class Comment(BaseModel):
    id: UUID = uuid4()
    task_id: UUID
    author_id: UUID
    body: str
    created_at: datetime = datetime.now()
    edited_at: Optional[datetime] = None