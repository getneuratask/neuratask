from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.user_entity import User
from src.ports.driven.pg_connection.user_repository import UserRepository
from src.ports.drivers.user_service import UserService


class UserServiceImpl(UserService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def get_all_users(self) -> List[User]:
        return self.user_repository.get_all()
    
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)

    def get_user_by_auth0_sub(self, auth0_sub: str) -> Optional[User]:
        return self.user_repository.get_by_auth0_sub(auth0_sub)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.get_by_email(email)
    
    def create_user(self, user: User) -> User:
        return self.user_repository.create(user)
    
    def update_user(self, user: User) -> Optional[User]:
        existing_user = self.user_repository.get_by_id(user.id)
        if not existing_user:
            return None
            
        user.updated_at = datetime.now()
        return self.user_repository.update(user)
    
    def delete_user(self, user_id: UUID) -> bool:
        return self.user_repository.delete(user_id)