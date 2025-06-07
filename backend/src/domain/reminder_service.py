from typing import List, Optional
from uuid import UUID

from src.domain.schemas.reminder_entity import Reminder
from src.ports.driven.reminder_repository import ReminderRepository
from src.ports.drivers.reminder_service import ReminderService


class ReminderServiceImpl(ReminderService):
    def __init__(self, reminder_repository: ReminderRepository):
        self.reminder_repository = reminder_repository
    
    def get_all_reminders(self) -> List[Reminder]:
        return self.reminder_repository.get_all()
    
    def get_reminder_by_id(self, reminder_id: UUID) -> Optional[Reminder]:
        return self.reminder_repository.get_by_id(reminder_id)
    
    def get_reminders_by_task(self, task_id: UUID) -> List[Reminder]:
        return self.reminder_repository.get_by_task(task_id)
    
    def get_reminders_by_user(self, user_id: UUID) -> List[Reminder]:
        return self.reminder_repository.get_by_user(user_id)
    
    def get_pending_reminders(self) -> List[Reminder]:
        return self.reminder_repository.get_pending_reminders()
    
    def create_reminder(self, reminder: Reminder) -> Reminder:
        return self.reminder_repository.create(reminder)
    
    def update_reminder(self, reminder: Reminder) -> Optional[Reminder]:
        existing_reminder = self.reminder_repository.get_by_id(reminder.id)
        if not existing_reminder:
            return None
        return self.reminder_repository.update(reminder)
    
    def delete_reminder(self, reminder_id: UUID) -> bool:
        return self.reminder_repository.delete(reminder_id)