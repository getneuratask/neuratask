from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime, date
from enum import Enum


class TaskStatus(str, Enum):
    TODO = 'TODO'
    DOING = 'DOING'
    DONE = 'DONE'


class Task(BaseModel):
    id: UUID = uuid4()
    project_id: UUID
    parent_task_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: int = 4
    due_date: Optional[date] = None
    start_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    created_by: UUID
    assigned_to: Optional[UUID] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None