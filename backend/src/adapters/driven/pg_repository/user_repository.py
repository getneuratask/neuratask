from typing import List, Optional
from uuid import UUID

from src.domain.schemas.user_entity import User
from src.ports.driven.pg_connection.user_repository import UserRepository
from src.adapters.driven.pg_repository.base_repository import PostgresBaseRepository


class PostgresUserRepository(PostgresBaseRepository, UserRepository):
    def __init__(self: dict):
        super().__init__()
        self.table = "users"

    def get_all(self) -> List[User]:
        query = f"SELECT * FROM {self.table}"
        results = self._execute_query(query)
        return [User(**result) for result in results]

    def get_by_id(self, id: UUID) -> Optional[User]:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        result = self._execute_single(query, (str(id),))
        return User(**result) if result else None

    def create(self, entity: User) -> User:
        result = self._create_entity(self.table, entity)
        return User(**result)

    def update(self, entity: User) -> Optional[User]:
        result = self._update_entity(self.table, entity)
        return User(**result) if result else None

    def delete(self, id: UUID) -> bool:
        return self._delete_entity(self.table, id)

    def get_by_auth0_sub(self, auth0_sub: str) -> Optional[User]:
        query = f"SELECT * FROM {self.table} WHERE auth0_sub = %s"
        result = self._execute_single(query, (auth0_sub,))
        return User(**result) if result else None

    def get_by_email(self, email: str) -> Optional[User]:
        query = f"SELECT * FROM {self.table} WHERE email = %s"
        result = self._execute_single(query, (email,))
        return User(**result) if result else None