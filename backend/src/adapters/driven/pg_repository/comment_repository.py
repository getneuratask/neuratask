from typing import List, Optional
from uuid import UUID

from src.domain.schemas.comment_entity import Comment
from src.ports.driven.pg_connection.comment_repository import CommentRepository
from src.adapters.driven.pg_repository.base_repository import PostgresBaseRepository


class PostgresCommentRepository(PostgresBaseRepository, CommentRepository):
    def __init__(self: dict):
        super().__init__()
        self.table = "comments"

    def get_all(self) -> List[Comment]:
        query = f"SELECT * FROM {self.table} ORDER BY created_at DESC"
        results = self._execute_query(query)
        return [Comment(**result) for result in results]

    def get_by_id(self, id: UUID) -> Optional[Comment]:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        result = self._execute_single(query, (str(id),))
        return Comment(**result) if result else None

    def create(self, entity: Comment) -> Comment:
        result = self._create_entity(self.table, entity)
        return Comment(**result)

    def update(self, entity: Comment) -> Optional[Comment]:
        result = self._update_entity(self.table, entity)
        return Comment(**result) if result else None

    def delete(self, id: UUID) -> bool:
        return self._delete_entity(self.table, id)

    def get_by_task(self, task_id: UUID) -> List[Comment]:
        query = f"SELECT * FROM {self.table} WHERE task_id = %s ORDER BY created_at DESC"
        results = self._execute_query(query, (str(task_id),))
        return [Comment(**result) for result in results]

    def get_by_author(self, author_id: UUID) -> List[Comment]:
        query = f"SELECT * FROM {self.table} WHERE author_id = %s ORDER BY created_at DESC"
        results = self._execute_query(query, (str(author_id),))
        return [Comment(**result) for result in results]