from pydantic import BaseModel
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime


class ReminderChannel(str, Enum):
    PUSH = 'PUSH'
    EMAIL = 'EMAIL'
    WEB = 'WEB'


class Reminder(BaseModel):
    id: UUID = uuid4()
    task_id: UUID
    user_id: UUID
    remind_at: datetime
    channel: ReminderChannel = ReminderChannel.PUSH