from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.activity_log_entity import ActivityLog


class ActivityLogRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[ActivityLog]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[ActivityLog]:
        pass
    
    @abstractmethod
    def create(self, entity: ActivityLog) -> ActivityLog:
        pass
    
    @abstractmethod
    def update(self, entity: ActivityLog) -> Optional[ActivityLog]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def get_by_entity(self, entity_type: str, entity_id: UUID) -> List[ActivityLog]:
        pass

    @abstractmethod
    def get_by_actor(self, actor_id: UUID) -> List[ActivityLog]:
        pass