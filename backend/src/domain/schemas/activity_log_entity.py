from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime


class ActivityLog(BaseModel):
    id: UUID = uuid4()
    entity_type: str
    entity_id: UUID
    action: str
    actor_id: UUID
    payload: Optional[Dict[str, Any]] = None
    created_at: datetime = datetime.now()