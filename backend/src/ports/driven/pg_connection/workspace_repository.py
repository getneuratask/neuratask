from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.workspace_entity import Workspace


class WorkspaceRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Workspace]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Workspace]:
        pass
    
    @abstractmethod
    def create(self, entity: Workspace) -> Workspace:
        pass
    
    @abstractmethod
    def update(self, entity: Workspace) -> Optional[Workspace]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def get_by_owner(self, owner_id: UUID) -> List[Workspace]:
        pass