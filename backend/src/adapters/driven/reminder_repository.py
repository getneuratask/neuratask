from typing import List, Optional
from uuid import UUID
from datetime import datetime

from src.domain.schemas.reminder_entity import Reminder
from src.ports.driven.repository import ReminderRepository
from src.adapters.driven.base_repository import PostgresBaseRepository


class PostgresReminderRepository(PostgresBaseRepository, ReminderRepository):
    def __init__(self, connection_params: dict):
        super().__init__(connection_params)
        self.table = "reminders"

    def get_all(self) -> List[Reminder]:
        query = f"SELECT * FROM {self.table} ORDER BY remind_at"
        results = self._execute_query(query)
        return [Reminder(**result) for result in results]

    def get_by_id(self, id: UUID) -> Optional[Reminder]:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        result = self._execute_single(query, (str(id),))
        return Reminder(**result) if result else None

    def create(self, reminder: Reminder) -> Reminder:
        result = self._create_entity(self.table, reminder)
        return Reminder(**result)

    def update(self, reminder: Reminder) -> Optional[Reminder]:
        result = self._update_entity(self.table, reminder)
        return Reminder(**result) if result else None

    def delete(self, id: UUID) -> bool:
        return self._delete_entity(self.table, id)

    def get_by_task(self, task_id: UUID) -> List[Reminder]:
        query = f"SELECT * FROM {self.table} WHERE task_id = %s ORDER BY remind_at"
        results = self._execute_query(query, (str(task_id),))
        return [Reminder(**result) for result in results]

    def get_by_user(self, user_id: UUID) -> List[Reminder]:
        query = f"SELECT * FROM {self.table} WHERE user_id = %s ORDER BY remind_at"
        results = self._execute_query(query, (str(user_id),))
        return [Reminder(**result) for result in results]

    def get_pending_reminders(self) -> List[Reminder]:
        query = f"""
            SELECT * FROM {self.table} 
            WHERE remind_at > NOW() 
            ORDER BY remind_at
        """
        results = self._execute_query(query)
        return [Reminder(**result) for result in results]