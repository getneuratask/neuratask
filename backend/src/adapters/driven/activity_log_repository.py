from typing import List, Optional
from uuid import UUID

from src.domain.schemas.activity_log_entity import ActivityLog
from src.ports.driven.activity_log_repository import ActivityLogRepository
from src.adapters.driven.base_repository import PostgresBaseRepository


class PostgresActivityLogRepository(PostgresBaseRepository, ActivityLogRepository):
    def __init__(self, connection_params: dict):
        super().__init__(connection_params)
        self.table = "activity_log"

    def get_all(self) -> List[ActivityLog]:
        query = f"SELECT * FROM {self.table} ORDER BY created_at DESC"
        results = self._execute_query(query)
        return [ActivityLog(**result) for result in results]

    def get_by_id(self, id: UUID) -> Optional[ActivityLog]:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        result = self._execute_single(query, (str(id),))
        return ActivityLog(**result) if result else None

    def create(self, entity: ActivityLog) -> ActivityLog:
        result = self._create_entity(self.table, entity)
        return ActivityLog(**result)

    def update(self, entity: ActivityLog) -> Optional[ActivityLog]:
        result = self._update_entity(self.table, entity)
        return ActivityLog(**result) if result else None

    def delete(self, id: UUID) -> bool:
        return self._delete_entity(self.table, id)

    def get_by_entity(self, entity_type: str, entity_id: UUID) -> List[ActivityLog]:
        query = f"""
            SELECT * FROM {self.table} 
            WHERE entity_type = %s AND entity_id = %s 
            ORDER BY created_at DESC
        """
        results = self._execute_query(query, (entity_type, str(entity_id)))
        return [ActivityLog(**result) for result in results]

    def get_by_actor(self, actor_id: UUID) -> List[ActivityLog]:
        query = f"SELECT * FROM {self.table} WHERE actor_id = %s ORDER BY created_at DESC"
        results = self._execute_query(query, (str(actor_id),))
        return [ActivityLog(**result) for result in results]