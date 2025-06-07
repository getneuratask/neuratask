from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.comment_entity import Comment


class CommentService(ABC):
    @abstractmethod
    def get_all_comments(self) -> List[Comment]:
        pass

    @abstractmethod
    def get_comment_by_id(self, comment_id: UUID) -> Optional[Comment]:
        pass

    @abstractmethod
    def get_comments_by_task(self, task_id: UUID) -> List[Comment]:
        pass

    @abstractmethod
    def get_comments_by_author(self, author_id: UUID) -> List[Comment]:
        pass

    @abstractmethod
    def create_comment(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    def update_comment(self, comment: Comment) -> Optional[Comment]:
        pass

    @abstractmethod
    def delete_comment(self, comment_id: UUID) -> bool:
        pass