"""
User endpoints for the NeuralTask API
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from src.domain.schemas import User
from src.ports.drivers import UserService
from .dependencies import get_user_service
from .dtos import UserCreateDTO, UserUpdateDTO

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=List[User])
def get_all_users(service: UserService = Depends(get_user_service)):
    """Get all users"""
    return service.get_all_users()

@router.get("/{user_id}", response_model=User)
def get_user_by_id(user_id: UUID, service: UserService = Depends(get_user_service)):
    """Get user by ID"""
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/auth0/{auth0_sub}", response_model=User)
def get_user_by_auth0_sub(auth0_sub: str, service: UserService = Depends(get_user_service)):
    """Get user by Auth0 subject"""
    user = service.get_user_by_auth0_sub(auth0_sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/email/{email}", response_model=User)
def get_user_by_email(email: str, service: UserService = Depends(get_user_service)):
    """Get user by email"""
    user = service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", response_model=User, status_code=201)
def create_user(user_data: UserCreateDTO, service: UserService = Depends(get_user_service)):
    """Create a new user"""
    user = User(**user_data.dict())
    return service.create_user(user)

@router.put("/{user_id}", response_model=User)
def update_user(user_id: UUID, user_data: UserUpdateDTO, service: UserService = Depends(get_user_service)):
    """Update user"""
    existing_user = service.get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_user, key, value)
    
    updated_user = service.update_user(existing_user)
    if not updated_user:
        raise HTTPException(status_code=400, detail="Failed to update user")
    return updated_user

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    """Delete user"""
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
