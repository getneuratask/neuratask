from typing import List, Optional
from uuid import UUID

from src.domain.schemas.label_entity import Label
from src.ports.driven.label_repository import LabelRepository
from src.adapters.driven.base_repository import PostgresBaseRepository


class PostgresLabelRepository(PostgresBaseRepository, LabelRepository):
    def __init__(self, connection_params: dict):
        super().__init__(connection_params)
        self.table = "labels"

    def get_all(self) -> List[Label]:
        query = f"SELECT * FROM {self.table}"
        results = self._execute_query(query)
        return [Label(**result) for result in results]

    def get_by_id(self, id: UUID) -> Optional[Label]:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        result = self._execute_single(query, (str(id),))
        return Label(**result) if result else None

    def create(self, entity: Label) -> Label:
        result = self._create_entity(self.table, entity)
        return Label(**result)

    def update(self, entity: Label) -> Optional[Label]:
        result = self._update_entity(self.table, entity)
        return Label(**result) if result else None

    def delete(self, id: UUID) -> bool:
        return self._delete_entity(self.table, id)

    def get_by_workspace(self, workspace_id: UUID) -> List[Label]:
        query = f"SELECT * FROM {self.table} WHERE workspace_id = %s"
        results = self._execute_query(query, (str(workspace_id),))
        return [Label(**result) for result in results]

    def get_by_task(self, task_id: UUID) -> List[Label]:
        query = f"""
            SELECT l.* FROM {self.table} l
            INNER JOIN task_labels tl ON tl.label_id = l.id
            WHERE tl.task_id = %s
        """
        results = self._execute_query(query, (str(task_id),))
        return [Label(**result) for result in results]