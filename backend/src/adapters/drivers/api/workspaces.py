"""
Workspace endpoints for the NeuralTask API
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from src.domain.schemas import Workspace
from src.ports.drivers import WorkspaceService
from .dependencies import get_workspace_service
from .dtos import WorkspaceCreateDTO, WorkspaceUpdateDTO

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

@router.get("", response_model=List[Workspace])
def get_all_workspaces(service: WorkspaceService = Depends(get_workspace_service)):
    """Get all workspaces"""
    return service.get_all_workspaces()

@router.get("/{workspace_id}", response_model=Workspace)
def get_workspace_by_id(workspace_id: UUID, service: WorkspaceService = Depends(get_workspace_service)):
    """Get workspace by ID"""
    workspace = service.get_workspace_by_id(workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.post("", response_model=Workspace, status_code=201)
def create_workspace(workspace_data: WorkspaceCreateDTO, service: WorkspaceService = Depends(get_workspace_service)):
    """Create a new workspace"""
    workspace = Workspace(**workspace_data.dict())
    return service.create_workspace(workspace)

@router.put("/{workspace_id}", response_model=Workspace)
def update_workspace(workspace_id: UUID, workspace_data: WorkspaceUpdateDTO, service: WorkspaceService = Depends(get_workspace_service)):
    """Update workspace"""
    existing_workspace = service.get_workspace_by_id(workspace_id)
    if not existing_workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    update_data = workspace_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_workspace, key, value)
    
    updated_workspace = service.update_workspace(existing_workspace)
    if not updated_workspace:
        raise HTTPException(status_code=400, detail="Failed to update workspace")
    return updated_workspace

@router.delete("/{workspace_id}", status_code=204)
def delete_workspace(workspace_id: UUID, service: WorkspaceService = Depends(get_workspace_service)):
    """Delete workspace"""
    success = service.delete_workspace(workspace_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workspace not found")

# Related endpoints
@router.get("/{workspace_id}/owner/{owner_id}", response_model=List[Workspace])
def get_workspaces_by_owner(owner_id: UUID, service: WorkspaceService = Depends(get_workspace_service)):
    """Get workspaces by owner"""
    return service.get_workspaces_by_owner(owner_id)
