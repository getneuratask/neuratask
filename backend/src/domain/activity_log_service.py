from typing import List, Optional
from uuid import UUID

from src.domain.schemas.activity_log_entity import ActivityLog
from src.ports.driven.activity_log_repository import ActivityLogRepository
from src.ports.drivers.activity_log_service import ActivityLogService


class ActivityLogServiceImpl(ActivityLogService):
    def __init__(self, activity_log_repository: ActivityLogRepository):
        self.activity_log_repository = activity_log_repository
    
    def get_all_activities(self) -> List[ActivityLog]:
        return self.activity_log_repository.get_all()
    
    def get_activity_by_id(self, activity_id: UUID) -> Optional[ActivityLog]:
        return self.activity_log_repository.get_by_id(activity_id)
    
    def get_activities_by_entity(self, entity_type: str, entity_id: UUID) -> List[ActivityLog]:
        return self.activity_log_repository.get_by_entity(entity_type, entity_id)
    
    def get_activities_by_actor(self, actor_id: UUID) -> List[ActivityLog]:
        return self.activity_log_repository.get_by_actor(actor_id)
    
    def create_activity(self, activity: ActivityLog) -> ActivityLog:
        return self.activity_log_repository.create(activity)
    
    def delete_activity(self, activity_id: UUID) -> bool:
        return self.activity_log_repository.delete(activity_id)