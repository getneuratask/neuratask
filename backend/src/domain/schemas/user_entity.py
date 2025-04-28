from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


class User(BaseModel):
    id: UUID = uuid4()
    auth0_sub: str
    name: str
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None