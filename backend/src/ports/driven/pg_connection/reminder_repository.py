from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.reminder_entity import Reminder


class ReminderRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Reminder]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Reminder]:
        pass
    
    @abstractmethod
    def create(self, entity: Reminder) -> Reminder:
        pass
    
    @abstractmethod
    def update(self, entity: Reminder) -> Optional[Reminder]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def get_by_task(self, task_id: UUID) -> List[Reminder]:
        pass

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> List[Reminder]:
        pass

    @abstractmethod
    def get_pending_reminders(self) -> List[Reminder]:
        """Get reminders that haven't been triggered yet"""
        pass