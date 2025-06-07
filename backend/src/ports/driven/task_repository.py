from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.task_entity import Task


class TaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Task]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Task]:
        pass
    
    @abstractmethod
    def create(self, entity: Task) -> Task:
        pass
    
    @abstractmethod
    def update(self, entity: Task) -> Optional[Task]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def get_by_project_id(self, project_id: UUID) -> List[Task]:
        pass

    @abstractmethod
    def get_by_assigned_user(self, user_id: UUID) -> List[Task]:
        pass

    @abstractmethod
    def get_by_parent_task(self, parent_task_id: UUID) -> List[Task]:
        pass