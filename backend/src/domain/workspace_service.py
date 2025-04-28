from typing import List, Optional
from uuid import UUID

from src.domain.schemas.workspace_entity import Workspace
from src.ports.driven.repository import WorkspaceRepository
from src.ports.drivers.task_service import WorkspaceService


class WorkspaceServiceImpl(WorkspaceService):
    def __init__(self, workspace_repository: WorkspaceRepository):
        self.workspace_repository = workspace_repository
    
    def get_all_workspaces(self) -> List[Workspace]:
        return self.workspace_repository.get_all()
    
    def get_workspace_by_id(self, workspace_id: UUID) -> Optional[Workspace]:
        return self.workspace_repository.get_by_id(workspace_id)
    
    def get_workspaces_by_owner(self, owner_id: UUID) -> List[Workspace]:
        return self.workspace_repository.get_by_owner(owner_id)
    
    def create_workspace(self, workspace: Workspace) -> Workspace:
        return self.workspace_repository.create(workspace)
    
    def update_workspace(self, workspace: Workspace) -> Optional[Workspace]:
        existing_workspace = self.workspace_repository.get_by_id(workspace.id)
        if not existing_workspace:
            return None
        return self.workspace_repository.update(workspace)
    
    def delete_workspace(self, workspace_id: UUID) -> bool:
        return self.workspace_repository.delete(workspace_id)