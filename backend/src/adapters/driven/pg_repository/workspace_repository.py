from typing import List, Optional
from uuid import UUID

from src.domain.schemas.workspace_entity import Workspace
from src.ports.driven.pg_connection.workspace_repository import WorkspaceRepository
from src.adapters.driven.pg_repository.base_repository import PostgresBaseRepository


class PostgresWorkspaceRepository(PostgresBaseRepository, WorkspaceRepository):
    def __init__(self: dict):
        super().__init__()
        self.table = "workspaces"

    def get_all(self) -> List[Workspace]:
        query = f"SELECT * FROM {self.table}"
        results = self._execute_query(query)
        return [Workspace(**result) for result in results]

    def get_by_id(self, id: UUID) -> Optional[Workspace]:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        result = self._execute_single(query, (str(id),))
        return Workspace(**result) if result else None

    def create(self, entity: Workspace) -> Workspace:
        result = self._create_entity(self.table, entity)
        return Workspace(**result)

    def update(self, entity: Workspace) -> Optional[Workspace]:
        result = self._update_entity(self.table, entity)
        return Workspace(**result) if result else None

    def delete(self, id: UUID) -> bool:
        return self._delete_entity(self.table, id)

    def get_by_owner(self, owner_id: UUID) -> List[Workspace]:
        query = f"SELECT * FROM {self.table} WHERE owner_id = %s"
        results = self._execute_query(query, (str(owner_id),))
        return [Workspace(**result) for result in results]