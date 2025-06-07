from typing import List, Optional
from uuid import UUID

from src.domain.schemas.project_entity import Project
from src.ports.driven.pg_connection.project_repository import ProjectRepository
from src.adapters.driven.pg_repository.base_repository import PostgresBaseRepository


class PostgresProjectRepository(PostgresBaseRepository, ProjectRepository):
    def __init__(self: dict):
        super().__init__()
        self.table = "projects"

    def get_all(self) -> List[Project]:
        query = f"SELECT * FROM {self.table}"
        results = self._execute_query(query)
        return [Project(**result) for result in results]

    def get_by_id(self, id: UUID) -> Optional[Project]:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        result = self._execute_single(query, (str(id),))
        return Project(**result) if result else None

    def create(self, entity: Project) -> Project:
        result = self._create_entity(self.table, entity)
        return Project(**result)

    def update(self, entity: Project) -> Optional[Project]:
        result = self._update_entity(self.table, entity)
        return Project(**result) if result else None

    def delete(self, id: UUID) -> bool:
        return self._delete_entity(self.table, id)

    def get_by_workspace(self, workspace_id: UUID) -> List[Project]:
        query = f"SELECT * FROM {self.table} WHERE workspace_id = %s ORDER BY sort_order"
        results = self._execute_query(query, (str(workspace_id),))
        return [Project(**result) for result in results]

    def get_active_by_workspace(self, workspace_id: UUID) -> List[Project]:
        query = f"""
            SELECT * FROM {self.table} 
            WHERE workspace_id = %s AND is_archived = FALSE 
            ORDER BY sort_order
        """
        results = self._execute_query(query, (str(workspace_id),))
        return [Project(**result) for result in results]