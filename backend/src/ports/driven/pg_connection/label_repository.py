from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.label_entity import Label


class LabelRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Label]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Label]:
        pass
    
    @abstractmethod
    def create(self, entity: Label) -> Label:
        pass
    
    @abstractmethod
    def update(self, entity: Label) -> Optional[Label]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def get_by_workspace(self, workspace_id: UUID) -> List[Label]:
        pass

    @abstractmethod
    def get_by_task(self, task_id: UUID) -> List[Label]:
        pass