from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.user_entity import User


class UserRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[User]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[User]:
        pass
    
    @abstractmethod
    def create(self, entity: User) -> User:
        pass
    
    @abstractmethod
    def update(self, entity: User) -> Optional[User]:
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def get_by_auth0_sub(self, auth0_sub: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass