from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.project_entity import Project


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