from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.reminder_entity import Reminder


class ReminderService(ABC):
    @abstractmethod
    def get_all_reminders(self) -> List[Reminder]:
        pass

    @abstractmethod
    def get_reminder_by_id(self, reminder_id: UUID) -> Optional[Reminder]:
        pass

    @abstractmethod
    def get_reminders_by_task(self, task_id: UUID) -> List[Reminder]:
        pass

    @abstractmethod
    def get_reminders_by_user(self, user_id: UUID) -> List[Reminder]:
        pass

    @abstractmethod
    def get_pending_reminders(self) -> List[Reminder]:
        pass

    @abstractmethod
    def create_reminder(self, reminder: Reminder) -> Reminder:
        pass

    @abstractmethod
    def update_reminder(self, reminder: Reminder) -> Optional[Reminder]:
        pass

    @abstractmethod
    def delete_reminder(self, reminder_id: UUID) -> bool:
        pass