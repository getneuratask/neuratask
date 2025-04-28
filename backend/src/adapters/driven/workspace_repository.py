from typing import List, Optional
from uuid import UUID

from src.domain.schemas.workspace_entity import Workspace
from src.ports.driven.repository import WorkspaceRepository
from src.adapters.driven.base_repository import PostgresBaseRepository


class PostgresWorkspaceRepository(PostgresBaseRepository, WorkspaceRepository):
    def __init__(self, connection_params: dict):
        super().__init__(connection_params)
        self.table = "workspaces"

    def get_all(self) -> List[Workspace]:
        query = f"SELECT * FROM {self.table}"
        results = self._execute_query(query)
        return [Workspace(**result) for result in results]

    def get_by_id(self, id: UUID) -> Optional[Workspace]:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        result = self._execute_single(query, (str(id),))
        return Workspace(**result) if result else None

    def create(self, workspace: Workspace) -> Workspace:
        result = self._create_entity(self.table, workspace)
        return Workspace(**result)

    def update(self, workspace: Workspace) -> Optional[Workspace]:
        result = self._update_entity(self.table, workspace)
        return Workspace(**result) if result else None

    def delete(self, id: UUID) -> bool:
        return self._delete_entity(self.table, id)

    def get_by_owner(self, owner_id: UUID) -> List[Workspace]:
        query = f"SELECT * FROM {self.table} WHERE owner_id = %s"
        results = self._execute_query(query, (str(owner_id),))
        return [Workspace(**result) for result in results]