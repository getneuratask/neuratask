from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.project_entity import Project


class ProjectRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Project]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Project]:
        pass
    
    @abstractmethod
    def create(self, entity: Project) -> Project:
        pass
    
    @abstractmethod
    def update(self, entity: Project) -> Optional[Project]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def get_by_workspace(self, workspace_id: UUID) -> List[Project]:
        pass

    @abstractmethod
    def get_active_by_workspace(self, workspace_id: UUID) -> List[Project]:
        """Get non-archived projects in a workspace"""
        pass