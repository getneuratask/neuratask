from typing import List, Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from src.domain.entities import Task
from src.application.services import TaskService
from src.infrastructure.repositories import InMemoryTaskRepository


app = FastAPI(title="NeuralTask API - Hexagonal Architecture")

# DTOs (Data Transfer Objects)
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# Dependency Injection
def get_task_service() -> TaskService:
    repository = InMemoryTaskRepository()
    return TaskService(repository)


# API Endpoints
@app.get("/tasks", response_model=List[Task])
def get_all_tasks(task_service: TaskService = Depends(get_task_service)):
    return task_service.get_all_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task_by_id(task_id: UUID, task_service: TaskService = Depends(get_task_service)):
    task = task_service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_data: TaskCreate, task_service: TaskService = Depends(get_task_service)):
    task = Task(title=task_data.title, description=task_data.description)
    return task_service.create_task(task)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    task_service: TaskService = Depends(get_task_service)
):
    task = task_service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    updated_task = task_service.update_task(task)
    if updated_task is None:
        raise HTTPException(status_code=500, detail="Failed to update task")
    
    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: UUID, task_service: TaskService = Depends(get_task_service)):
    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")