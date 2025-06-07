"""
Task endpoints for the NeuralTask API
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, Query
from src.domain.schemas import Task
from src.ports.drivers import TaskService
from .dependencies import get_task_service
from .dtos import TaskCreateDTO, TaskUpdateDTO

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("", response_model=List[Task])
def get_all_tasks(service: TaskService = Depends(get_task_service)):
    """Get all tasks"""
    return service.get_all_tasks()

@router.get("/{task_id}", response_model=Task)
def get_task_by_id(task_id: UUID, service: TaskService = Depends(get_task_service)):
    """Get task by ID"""
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("", response_model=Task, status_code=201)
def create_task(
    task_data: TaskCreateDTO, 
    created_by: UUID = Query(..., description="ID of the user creating the task"),
    service: TaskService = Depends(get_task_service)
):
    """Create a new task"""
    task_dict = task_data.dict()
    task_dict['created_by'] = created_by
    task = Task(**task_dict)
    return service.create_task(task)

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_data: TaskUpdateDTO, service: TaskService = Depends(get_task_service)):
    """Update task"""
    existing_task = service.get_task_by_id(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_task, key, value)
    
    updated_task = service.update_task(existing_task)
    if not updated_task:
        raise HTTPException(status_code=400, detail="Failed to update task")
    return updated_task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    """Delete task"""
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

# Related endpoints
@router.get("/project/{project_id}", response_model=List[Task])
def get_tasks_by_project(project_id: UUID, service: TaskService = Depends(get_task_service)):
    """Get tasks by project"""
    return service.get_tasks_by_project(project_id)

@router.get("/user/{user_id}/assigned", response_model=List[Task])
def get_tasks_by_assigned_user(user_id: UUID, service: TaskService = Depends(get_task_service)):
    """Get tasks assigned to user"""
    return service.get_tasks_by_assigned_user(user_id)

@router.get("/{parent_task_id}/subtasks", response_model=List[Task])
def get_subtasks(parent_task_id: UUID, service: TaskService = Depends(get_task_service)):
    """Get subtasks of a task"""
    return service.get_subtasks(parent_task_id)
