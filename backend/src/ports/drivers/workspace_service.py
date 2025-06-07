from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.workspace_entity import Workspace


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