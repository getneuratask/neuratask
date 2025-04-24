from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities import Task


class TaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Task]:
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        pass
    
    @abstractmethod
    def create(self, task: Task) -> Task:
        pass
    
    @abstractmethod
    def update(self, task: Task) -> Optional[Task]:
        pass
    
    @abstractmethod
    def delete(self, task_id: UUID) -> bool:
        pass