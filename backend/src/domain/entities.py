from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


class Task(BaseModel):
    id: UUID = uuid4()
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None