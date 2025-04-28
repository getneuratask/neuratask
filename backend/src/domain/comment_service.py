from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.comment_entity import Comment
from src.ports.driven.repository import CommentRepository
from src.ports.drivers.task_service import CommentService


class CommentServiceImpl(CommentService):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository
    
    def get_all_comments(self) -> List[Comment]:
        return self.comment_repository.get_all()
    
    def get_comment_by_id(self, comment_id: UUID) -> Optional[Comment]:
        return self.comment_repository.get_by_id(comment_id)
    
    def get_comments_by_task(self, task_id: UUID) -> List[Comment]:
        return self.comment_repository.get_by_task(task_id)
    
    def get_comments_by_author(self, author_id: UUID) -> List[Comment]:
        return self.comment_repository.get_by_author(author_id)
    
    def create_comment(self, comment: Comment) -> Comment:
        return self.comment_repository.create(comment)
    
    def update_comment(self, comment: Comment) -> Optional[Comment]:
        existing_comment = self.comment_repository.get_by_id(comment.id)
        if not existing_comment:
            return None
            
        comment.edited_at = datetime.now()
        return self.comment_repository.update(comment)
    
    def delete_comment(self, comment_id: UUID) -> bool:
        return self.comment_repository.delete(comment_id)