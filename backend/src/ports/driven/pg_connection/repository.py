from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.task_entity import Task
from src.domain.schemas.user_entity import User
from src.domain.schemas.workspace_entity import Workspace
from src.domain.schemas.project_entity import Project
from src.domain.schemas.label_entity import Label
from src.domain.schemas.comment_entity import Comment
from src.domain.schemas.reminder_entity import Reminder
from src.domain.schemas.activity_log_entity import ActivityLog


class BaseRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[any]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[any]:
        pass
    
    @abstractmethod
    def create(self, entity: any) -> any:
        pass
    
    @abstractmethod
    def update(self, entity: any) -> Optional[any]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass


class TaskRepository(BaseRepository):
    @abstractmethod
    def get_by_project_id(self, project_id: UUID) -> List[Task]:
        pass

    @abstractmethod
    def get_by_assigned_user(self, user_id: UUID) -> List[Task]:
        pass

    @abstractmethod
    def get_by_parent_task(self, parent_task_id: UUID) -> List[Task]:
        pass


class UserRepository(BaseRepository):
    @abstractmethod
    def get_by_auth0_sub(self, auth0_sub: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass


class WorkspaceRepository(BaseRepository):
    @abstractmethod
    def get_by_owner(self, owner_id: UUID) -> List[Workspace]:
        pass


class ProjectRepository(BaseRepository):
    @abstractmethod
    def get_by_workspace(self, workspace_id: UUID) -> List[Project]:
        pass

    @abstractmethod
    def get_active_by_workspace(self, workspace_id: UUID) -> List[Project]:
        """Get non-archived projects in a workspace"""
        pass


class LabelRepository(BaseRepository):
    @abstractmethod
    def get_by_workspace(self, workspace_id: UUID) -> List[Label]:
        pass

    @abstractmethod
    def get_by_task(self, task_id: UUID) -> List[Label]:
        pass


class CommentRepository(BaseRepository):
    @abstractmethod
    def get_by_task(self, task_id: UUID) -> List[Comment]:
        pass

    @abstractmethod
    def get_by_author(self, author_id: UUID) -> List[Comment]:
        pass


class ReminderRepository(BaseRepository):
    @abstractmethod
    def get_by_task(self, task_id: UUID) -> List[Reminder]:
        pass

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> List[Reminder]:
        pass

    @abstractmethod
    def get_pending_reminders(self) -> List[Reminder]:
        """Get reminders that haven't been triggered yet"""
        pass


class ActivityLogRepository(BaseRepository):
    @abstractmethod
    def get_by_entity(self, entity_type: str, entity_id: UUID) -> List[ActivityLog]:
        pass

    @abstractmethod
    def get_by_actor(self, actor_id: UUID) -> List[ActivityLog]:
        pass