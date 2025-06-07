"""
Reminder endpoints for the NeuralTask API
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from src.domain.schemas import Reminder
from src.ports.drivers import ReminderService
from .dependencies import get_reminder_service
from .dtos import ReminderCreateDTO, ReminderUpdateDTO

router = APIRouter(prefix="/reminders", tags=["Reminders"])

@router.get("", response_model=List[Reminder])
def get_all_reminders(service: ReminderService = Depends(get_reminder_service)):
    """Get all reminders"""
    return service.get_all_reminders()

@router.get("/{reminder_id}", response_model=Reminder)
def get_reminder_by_id(reminder_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    """Get reminder by ID"""
    reminder = service.get_reminder_by_id(reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder

@router.get("/pending", response_model=List[Reminder])
def get_pending_reminders(service: ReminderService = Depends(get_reminder_service)):
    """Get pending reminders"""
    return service.get_pending_reminders()

@router.post("", response_model=Reminder, status_code=201)
def create_reminder(reminder_data: ReminderCreateDTO, service: ReminderService = Depends(get_reminder_service)):
    """Create a new reminder"""
    reminder = Reminder(**reminder_data.dict())
    return service.create_reminder(reminder)

@router.put("/{reminder_id}", response_model=Reminder)
def update_reminder(reminder_id: UUID, reminder_data: ReminderUpdateDTO, service: ReminderService = Depends(get_reminder_service)):
    """Update reminder"""
    existing_reminder = service.get_reminder_by_id(reminder_id)
    if not existing_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    update_data = reminder_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_reminder, key, value)
    
    updated_reminder = service.update_reminder(existing_reminder)
    if not updated_reminder:
        raise HTTPException(status_code=400, detail="Failed to update reminder")
    return updated_reminder

@router.delete("/{reminder_id}", status_code=204)
def delete_reminder(reminder_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    """Delete reminder"""
    success = service.delete_reminder(reminder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reminder not found")

# Related endpoints
@router.get("/task/{task_id}", response_model=List[Reminder])
def get_reminders_by_task(task_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    """Get reminders by task"""
    return service.get_reminders_by_task(task_id)

@router.get("/user/{user_id}", response_model=List[Reminder])
def get_reminders_by_user(user_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    """Get reminders by user"""
    return service.get_reminders_by_user(user_id)
