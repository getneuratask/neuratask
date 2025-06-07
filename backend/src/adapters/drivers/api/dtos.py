"""
Data Transfer Objects (DTOs) for API requests and responses
"""
from datetime import datetime, date
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, EmailStr
from src.domain.schemas import TaskStatus, ReminderChannel


# =====================================================
# USER DTOs
# =====================================================

class UserCreateDTO(BaseModel):
    auth0_sub: str
    name: str
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None

class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None


# =====================================================
# WORKSPACE DTOs
# =====================================================

class WorkspaceCreateDTO(BaseModel):
    name: str
    owner_id: UUID

class WorkspaceUpdateDTO(BaseModel):
    name: Optional[str] = None


# =====================================================
# PROJECT DTOs
# =====================================================

class ProjectCreateDTO(BaseModel):
    name: str
    workspace_id: UUID
    color: Optional[str] = None
    sort_order: int = 0

class ProjectUpdateDTO(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    sort_order: Optional[int] = None
    is_archived: Optional[bool] = None


# =====================================================
# TASK DTOs
# =====================================================

class TaskCreateDTO(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: UUID
    parent_task_id: Optional[UUID] = None
    priority: int = 4
    due_date: Optional[date] = None
    start_date: Optional[date] = None
    assigned_to: Optional[UUID] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None

class TaskUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = None
    due_date: Optional[date] = None
    start_date: Optional[date] = None
    assigned_to: Optional[UUID] = None
    is_recurring: Optional[bool] = None
    recurrence_rule: Optional[str] = None


# =====================================================
# LABEL DTOs
# =====================================================

class LabelCreateDTO(BaseModel):
    name: str
    workspace_id: UUID
    color: Optional[str] = None

class LabelUpdateDTO(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None


# =====================================================
# COMMENT DTOs
# =====================================================

class CommentCreateDTO(BaseModel):
    task_id: UUID
    author_id: UUID
    body: str

class CommentUpdateDTO(BaseModel):
    body: str


# =====================================================
# REMINDER DTOs
# =====================================================

class ReminderCreateDTO(BaseModel):
    task_id: UUID
    user_id: UUID
    remind_at: datetime
    channel: ReminderChannel = ReminderChannel.PUSH

class ReminderUpdateDTO(BaseModel):
    remind_at: Optional[datetime] = None
    channel: Optional[ReminderChannel] = None


# =====================================================
# ACTIVITY LOG DTOs
# =====================================================

class ActivityLogCreateDTO(BaseModel):
    entity_type: str
    entity_id: UUID
    action: str
    actor_id: UUID
    payload: Optional[Dict[str, Any]] = None
