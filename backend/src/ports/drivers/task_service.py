from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.task_entity import Task


class TaskService(ABC):
    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        pass
    
    @abstractmethod
    def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        pass
    
    @abstractmethod
    def get_tasks_by_project(self, project_id: UUID) -> List[Task]:
        pass
    
    @abstractmethod
    def get_tasks_by_assigned_user(self, user_id: UUID) -> List[Task]:
        pass
    
    @abstractmethod
    def get_subtasks(self, parent_task_id: UUID) -> List[Task]:
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