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


class TaskService(ABC):
    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        pass
    
    @abstractmethod
    def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        pass
    
    @abstractmethod
    def create_task(self, task: Task) -> Task:
        pass
    
    @abstractmethod
    def update_task(self, task: Task) -> Optional[Task]:
        pass
    
    @abstractmethod
    def delete_task(self, task_id: UUID) -> bool:
        pass


class UserService(ABC):
    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_auth0_sub(self, auth0_sub: str) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> Optional[User]:
        pass

    @abstractmethod
    def delete_user(self, user_id: UUID) -> bool:
        pass


class WorkspaceService(ABC):
    @abstractmethod
    def get_all_workspaces(self) -> List[Workspace]:
        pass

    @abstractmethod
    def get_workspace_by_id(self, workspace_id: UUID) -> Optional[Workspace]:
        pass

    @abstractmethod
    def get_workspaces_by_owner(self, owner_id: UUID) -> List[Workspace]:
        pass

    @abstractmethod
    def create_workspace(self, workspace: Workspace) -> Workspace:
        pass

    @abstractmethod
    def update_workspace(self, workspace: Workspace) -> Optional[Workspace]:
        pass

    @abstractmethod
    def delete_workspace(self, workspace_id: UUID) -> bool:
        pass


class ProjectService(ABC):
    @abstractmethod
    def get_all_projects(self) -> List[Project]:
        pass

    @abstractmethod
    def get_project_by_id(self, project_id: UUID) -> Optional[Project]:
        pass

    @abstractmethod
    def get_projects_by_workspace(self, workspace_id: UUID) -> List[Project]:
        pass

    @abstractmethod
    def get_active_projects_by_workspace(self, workspace_id: UUID) -> List[Project]:
        pass

    @abstractmethod
    def create_project(self, project: Project) -> Project:
        pass

    @abstractmethod
    def update_project(self, project: Project) -> Optional[Project]:
        pass

    @abstractmethod
    def delete_project(self, project_id: UUID) -> bool:
        pass


class LabelService(ABC):
    @abstractmethod
    def get_all_labels(self) -> List[Label]:
        pass

    @abstractmethod
    def get_label_by_id(self, label_id: UUID) -> Optional[Label]:
        pass

    @abstractmethod
    def get_labels_by_workspace(self, workspace_id: UUID) -> List[Label]:
        pass

    @abstractmethod
    def get_labels_by_task(self, task_id: UUID) -> List[Label]:
        pass

    @abstractmethod
    def create_label(self, label: Label) -> Label:
        pass

    @abstractmethod
    def update_label(self, label: Label) -> Optional[Label]:
        pass

    @abstractmethod
    def delete_label(self, label_id: UUID) -> bool:
        pass


class CommentService(ABC):
    @abstractmethod
    def get_all_comments(self) -> List[Comment]:
        pass

    @abstractmethod
    def get_comment_by_id(self, comment_id: UUID) -> Optional[Comment]:
        pass

    @abstractmethod
    def get_comments_by_task(self, task_id: UUID) -> List[Comment]:
        pass

    @abstractmethod
    def get_comments_by_author(self, author_id: UUID) -> List[Comment]:
        pass

    @abstractmethod
    def create_comment(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    def update_comment(self, comment: Comment) -> Optional[Comment]:
        pass

    @abstractmethod
    def delete_comment(self, comment_id: UUID) -> bool:
        pass


class ReminderService(ABC):
    @abstractmethod
    def get_all_reminders(self) -> List[Reminder]:
        pass

    @abstractmethod
    def get_reminder_by_id(self, reminder_id: UUID) -> Optional[Reminder]:
        pass

    @abstractmethod
    def get_reminders_by_task(self, task_id: UUID) -> List[Reminder]:
        pass

    @abstractmethod
    def get_reminders_by_user(self, user_id: UUID) -> List[Reminder]:
        pass

    @abstractmethod
    def get_pending_reminders(self) -> List[Reminder]:
        pass

    @abstractmethod
    def create_reminder(self, reminder: Reminder) -> Reminder:
        pass

    @abstractmethod
    def update_reminder(self, reminder: Reminder) -> Optional[Reminder]:
        pass

    @abstractmethod
    def delete_reminder(self, reminder_id: UUID) -> bool:
        pass


class ActivityLogService(ABC):
    @abstractmethod
    def get_all_activities(self) -> List[ActivityLog]:
        pass

    @abstractmethod
    def get_activity_by_id(self, activity_id: UUID) -> Optional[ActivityLog]:
        pass

    @abstractmethod
    def get_activities_by_entity(self, entity_type: str, entity_id: UUID) -> List[ActivityLog]:
        pass

    @abstractmethod
    def get_activities_by_actor(self, actor_id: UUID) -> List[ActivityLog]:
        pass

    @abstractmethod
    def create_activity(self, activity: ActivityLog) -> ActivityLog:
        pass

    @abstractmethod
    def delete_activity(self, activity_id: UUID) -> bool:
        pass