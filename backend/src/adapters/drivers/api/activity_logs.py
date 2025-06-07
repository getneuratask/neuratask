"""
Activity Log endpoints for the NeuralTask API
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from src.domain.schemas import ActivityLog
from src.ports.drivers import ActivityLogService
from .dependencies import get_activity_log_service
from .dtos import ActivityLogCreateDTO

router = APIRouter(prefix="/activity-logs", tags=["Activity Logs"])

@router.get("", response_model=List[ActivityLog])
def get_all_activities(service: ActivityLogService = Depends(get_activity_log_service)):
    """Get all activity logs"""
    return service.get_all_activities()

@router.get("/{activity_id}", response_model=ActivityLog)
def get_activity_by_id(activity_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    """Get activity log by ID"""
    activity = service.get_activity_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity log not found")
    return activity

@router.post("", response_model=ActivityLog, status_code=201)
def create_activity(activity_data: ActivityLogCreateDTO, service: ActivityLogService = Depends(get_activity_log_service)):
    """Create a new activity log entry"""
    activity = ActivityLog(**activity_data.dict())
    return service.create_activity(activity)

@router.delete("/{activity_id}", status_code=204)
def delete_activity(activity_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    """Delete activity log"""
    success = service.delete_activity(activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity log not found")

# Related endpoints
@router.get("/entity/{entity_type}/{entity_id}", response_model=List[ActivityLog])
def get_activities_by_entity(entity_type: str, entity_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    """Get activity logs by entity"""
    return service.get_activities_by_entity(entity_type, entity_id)

@router.get("/actor/{actor_id}", response_model=List[ActivityLog])
def get_activities_by_actor(actor_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    """Get activity logs by actor"""
    return service.get_activities_by_actor(actor_id)
