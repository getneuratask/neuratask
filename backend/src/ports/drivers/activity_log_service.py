from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.activity_log_entity import ActivityLog


class ActivityLogService(ABC):
    @abstractmethod
    def get_all_activities(self) -> List[ActivityLog]:
        pass

    @abstractmethod
    def get_activity_by_id(self, activity_id: UUID) -> Optional[ActivityLog]:
        pass

    @abstractmethod
    def get_activities_by_entity(self, entity_type: str, entity_id: UUID) -> List[ActivityLog]:
        pass

    @abstractmethod
    def get_activities_by_actor(self, actor_id: UUID) -> List[ActivityLog]:
        pass

    @abstractmethod
    def create_activity(self, activity: ActivityLog) -> ActivityLog:
        pass

    @abstractmethod
    def delete_activity(self, activity_id: UUID) -> bool:
        pass