from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.comment_entity import Comment


class CommentRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Comment]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Comment]:
        pass
    
    @abstractmethod
    def create(self, entity: Comment) -> Comment:
        pass
    
    @abstractmethod
    def update(self, entity: Comment) -> Optional[Comment]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def get_by_task(self, task_id: UUID) -> List[Comment]:
        pass

    @abstractmethod
    def get_by_author(self, author_id: UUID) -> List[Comment]:
        pass