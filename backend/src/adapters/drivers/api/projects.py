"""
Project endpoints for the NeuralTask API
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from src.domain.schemas import Project
from src.ports.drivers import ProjectService
from .dependencies import get_project_service
from .dtos import ProjectCreateDTO, ProjectUpdateDTO

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("", response_model=List[Project])
def get_all_projects(service: ProjectService = Depends(get_project_service)):
    """Get all projects"""
    return service.get_all_projects()

@router.get("/{project_id}", response_model=Project)
def get_project_by_id(project_id: UUID, service: ProjectService = Depends(get_project_service)):
    """Get project by ID"""
    project = service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("", response_model=Project, status_code=201)
def create_project(project_data: ProjectCreateDTO, service: ProjectService = Depends(get_project_service)):
    """Create a new project"""
    project = Project(**project_data.dict())
    return service.create_project(project)

@router.put("/{project_id}", response_model=Project)
def update_project(project_id: UUID, project_data: ProjectUpdateDTO, service: ProjectService = Depends(get_project_service)):
    """Update project"""
    existing_project = service.get_project_by_id(project_id)
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_project, key, value)
    
    updated_project = service.update_project(existing_project)
    if not updated_project:
        raise HTTPException(status_code=400, detail="Failed to update project")
    return updated_project

@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: UUID, service: ProjectService = Depends(get_project_service)):
    """Delete project"""
    success = service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")

# Related endpoints
@router.get("/workspace/{workspace_id}", response_model=List[Project])
def get_projects_by_workspace(workspace_id: UUID, service: ProjectService = Depends(get_project_service)):
    """Get projects by workspace"""
    return service.get_projects_by_workspace(workspace_id)

@router.get("/workspace/{workspace_id}/active", response_model=List[Project])
def get_active_projects_by_workspace(workspace_id: UUID, service: ProjectService = Depends(get_project_service)):
    """Get active projects by workspace"""
    return service.get_active_projects_by_workspace(workspace_id)
