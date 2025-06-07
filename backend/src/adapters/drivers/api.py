from typing import List, Optional, Dict, Any
from uuid import UUID
import os
from dotenv import load_dotenv
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from src.domain.schemas import *
from src.domain import *
from src.adapters.driven import *
from src.ports.drivers import *

# Load environment variables
load_dotenv()

# Database connection parameters
DB_PARAMS = {
    "dbname": os.getenv("NEURATASK_DB", "neuratask_db"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.getenv("PGPASSWORD", "postgres"),
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432")
}

app = FastAPI(title="NeuraTask API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DTOs
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: UUID
    parent_task_id: Optional[UUID] = None

class UserCreate(BaseModel):
    auth0_sub: str
    name: str
    email: Optional[EmailStr] = None

class WorkspaceCreate(BaseModel):
    name: str
    owner_id: UUID

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    workspace_id: UUID
    color: Optional[str] = None

class LabelCreate(BaseModel):
    name: str
    color: str
    workspace_id: UUID

class CommentCreate(BaseModel):
    content: str
    task_id: UUID
    author_id: UUID

class ReminderCreate(BaseModel):
    task_id: UUID
    user_id: UUID
    reminder_time: datetime
    message: Optional[str] = None

class ActivityLogCreate(BaseModel):
    entity_type: str
    entity_id: UUID
    action: str
    actor_id: UUID
    details: Optional[dict] = None

# Dependency injection
def get_task_service() -> TaskService:
    repository = PostgresTaskRepository(DB_PARAMS)
    return TaskServiceImpl(repository)

def get_user_service() -> UserService:
    repository = PostgresUserRepository(DB_PARAMS)
    return UserServiceImpl(repository)

def get_workspace_service() -> WorkspaceService:
    repository = PostgresWorkspaceRepository(DB_PARAMS)
    return WorkspaceServiceImpl(repository)

def get_project_service() -> ProjectService:
    repository = PostgresProjectRepository(DB_PARAMS)
    return ProjectServiceImpl(repository)

def get_label_service() -> LabelService:
    repository = PostgresLabelRepository(DB_PARAMS)
    return LabelServiceImpl(repository)

def get_comment_service() -> CommentService:
    repository = PostgresCommentRepository(DB_PARAMS)
    return CommentServiceImpl(repository)

def get_reminder_service() -> ReminderService:
    repository = PostgresReminderRepository(DB_PARAMS)
    return ReminderServiceImpl(repository)

def get_activity_log_service() -> ActivityLogService:
    repository = PostgresActivityLogRepository(DB_PARAMS)
    return ActivityLogServiceImpl(repository)

# Essential endpoints
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Task endpoints
@app.get("/tasks", response_model=List[Task])
def get_tasks(service: TaskService = Depends(get_task_service)):
    return service.get_all_tasks()

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

@app.get("/projects/{project_id}/tasks", response_model=List[Task])
def get_tasks_by_project(project_id: UUID, service: TaskService = Depends(get_task_service)):
    return service.get_tasks_by_project(project_id)

@app.get("/users/{user_id}/assigned-tasks", response_model=List[Task])
def get_tasks_by_assigned_user(user_id: UUID, service: TaskService = Depends(get_task_service)):
    return service.get_tasks_by_assigned_user(user_id)

@app.get("/tasks/{task_id}/subtasks", response_model=List[Task])
def get_subtasks(task_id: UUID, service: TaskService = Depends(get_task_service)):
    return service.get_subtasks(task_id)

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate, service: TaskService = Depends(get_task_service)):
    task = Task(**data.dict())
    return service.create_task(task)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, data: TaskCreate, service: TaskService = Depends(get_task_service)):
    task = Task(id=task_id, **data.dict())
    updated_task = service.update_task(task)
    if not updated_task:
        raise HTTPException(404, "Task not found")
    return updated_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    if not service.delete_task(task_id):
        raise HTTPException(404, "Task not found")
    return {"message": "Task deleted successfully"}

# User endpoints
@app.get("/users", response_model=List[User])
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@app.get("/users/auth0/{auth0_sub}", response_model=User)
def get_user_by_auth0(auth0_sub: str, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_auth0_sub(auth0_sub)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@app.get("/users/email/{email}", response_model=User)
def get_user_by_email(email: str, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_email(email)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@app.post("/users", response_model=User, status_code=201)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    user = User(**data.dict())
    return service.create_user(user)

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, data: UserCreate, service: UserService = Depends(get_user_service)):
    user = User(id=user_id, **data.dict())
    updated_user = service.update_user(user)
    if not updated_user:
        raise HTTPException(404, "User not found")
    return updated_user

@app.delete("/users/{user_id}")
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    if not service.delete_user(user_id):
        raise HTTPException(404, "User not found")
    return {"message": "User deleted successfully"}

# Workspace endpoints
@app.get("/workspaces", response_model=List[Workspace])
def get_workspaces(service: WorkspaceService = Depends(get_workspace_service)):
    return service.get_all_workspaces()

@app.get("/workspaces/{workspace_id}", response_model=Workspace)
def get_workspace(workspace_id: UUID, service: WorkspaceService = Depends(get_workspace_service)):
    workspace = service.get_workspace_by_id(workspace_id)
    if not workspace:
        raise HTTPException(404, "Workspace not found")
    return workspace

@app.get("/users/{user_id}/workspaces", response_model=List[Workspace])
def get_workspaces_by_user(user_id: UUID, service: WorkspaceService = Depends(get_workspace_service)):
    return service.get_workspaces_by_owner(user_id)

@app.post("/workspaces", response_model=Workspace, status_code=201)
def create_workspace(data: WorkspaceCreate, service: WorkspaceService = Depends(get_workspace_service)):
    workspace = Workspace(**data.dict())
    return service.create_workspace(workspace)

@app.put("/workspaces/{workspace_id}", response_model=Workspace)
def update_workspace(workspace_id: UUID, data: WorkspaceCreate, service: WorkspaceService = Depends(get_workspace_service)):
    workspace = Workspace(id=workspace_id, **data.dict())
    updated_workspace = service.update_workspace(workspace)
    if not updated_workspace:
        raise HTTPException(404, "Workspace not found")
    return updated_workspace

@app.delete("/workspaces/{workspace_id}")
def delete_workspace(workspace_id: UUID, service: WorkspaceService = Depends(get_workspace_service)):
    if not service.delete_workspace(workspace_id):
        raise HTTPException(404, "Workspace not found")
    return {"message": "Workspace deleted successfully"}

# Project endpoints
@app.get("/projects", response_model=List[Project])
def get_projects(service: ProjectService = Depends(get_project_service)):
    return service.get_all_projects()

@app.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: UUID, service: ProjectService = Depends(get_project_service)):
    project = service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    return project

@app.get("/workspaces/{workspace_id}/projects", response_model=List[Project])
def get_projects_by_workspace(workspace_id: UUID, service: ProjectService = Depends(get_project_service)):
    return service.get_projects_by_workspace(workspace_id)

@app.get("/workspaces/{workspace_id}/projects/active", response_model=List[Project])
def get_active_projects_by_workspace(workspace_id: UUID, service: ProjectService = Depends(get_project_service)):
    return service.get_active_projects_by_workspace(workspace_id)

@app.post("/projects", response_model=Project, status_code=201)
def create_project(data: ProjectCreate, service: ProjectService = Depends(get_project_service)):
    project = Project(**data.dict())
    return service.create_project(project)

@app.put("/projects/{project_id}", response_model=Project)
def update_project(project_id: UUID, data: ProjectCreate, service: ProjectService = Depends(get_project_service)):
    project = Project(id=project_id, **data.dict())
    updated_project = service.update_project(project)
    if not updated_project:
        raise HTTPException(404, "Project not found")
    return updated_project

@app.delete("/projects/{project_id}")
def delete_project(project_id: UUID, service: ProjectService = Depends(get_project_service)):
    if not service.delete_project(project_id):
        raise HTTPException(404, "Project not found")
    return {"message": "Project deleted successfully"}

# Label endpoints
@app.get("/labels", response_model=List[Label])
def get_labels(service: LabelService = Depends(get_label_service)):
    return service.get_all_labels()

@app.get("/labels/{label_id}", response_model=Label)
def get_label(label_id: UUID, service: LabelService = Depends(get_label_service)):
    label = service.get_label_by_id(label_id)
    if not label:
        raise HTTPException(404, "Label not found")
    return label

@app.get("/workspaces/{workspace_id}/labels", response_model=List[Label])
def get_labels_by_workspace(workspace_id: UUID, service: LabelService = Depends(get_label_service)):
    return service.get_labels_by_workspace(workspace_id)

@app.get("/tasks/{task_id}/labels", response_model=List[Label])
def get_labels_by_task(task_id: UUID, service: LabelService = Depends(get_label_service)):
    return service.get_labels_by_task(task_id)

@app.post("/labels", response_model=Label, status_code=201)
def create_label(data: LabelCreate, service: LabelService = Depends(get_label_service)):
    label = Label(**data.dict())
    return service.create_label(label)

@app.put("/labels/{label_id}", response_model=Label)
def update_label(label_id: UUID, data: LabelCreate, service: LabelService = Depends(get_label_service)):
    label = Label(id=label_id, **data.dict())
    updated_label = service.update_label(label)
    if not updated_label:
        raise HTTPException(404, "Label not found")
    return updated_label

@app.delete("/labels/{label_id}")
def delete_label(label_id: UUID, service: LabelService = Depends(get_label_service)):
    if not service.delete_label(label_id):
        raise HTTPException(404, "Label not found")
    return {"message": "Label deleted successfully"}

# Comment endpoints
@app.get("/comments", response_model=List[Comment])
def get_comments(service: CommentService = Depends(get_comment_service)):
    return service.get_all_comments()

@app.get("/comments/{comment_id}", response_model=Comment)
def get_comment(comment_id: UUID, service: CommentService = Depends(get_comment_service)):
    comment = service.get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(404, "Comment not found")
    return comment

@app.get("/tasks/{task_id}/comments", response_model=List[Comment])
def get_comments_by_task(task_id: UUID, service: CommentService = Depends(get_comment_service)):
    return service.get_comments_by_task(task_id)

@app.get("/users/{author_id}/comments", response_model=List[Comment])
def get_comments_by_author(author_id: UUID, service: CommentService = Depends(get_comment_service)):
    return service.get_comments_by_author(author_id)

@app.post("/comments", response_model=Comment, status_code=201)
def create_comment(data: CommentCreate, service: CommentService = Depends(get_comment_service)):
    comment = Comment(**data.dict())
    return service.create_comment(comment)

@app.put("/comments/{comment_id}", response_model=Comment)
def update_comment(comment_id: UUID, data: CommentCreate, service: CommentService = Depends(get_comment_service)):
    comment = Comment(id=comment_id, **data.dict())
    updated_comment = service.update_comment(comment)
    if not updated_comment:
        raise HTTPException(404, "Comment not found")
    return updated_comment

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: UUID, service: CommentService = Depends(get_comment_service)):
    if not service.delete_comment(comment_id):
        raise HTTPException(404, "Comment not found")
    return {"message": "Comment deleted successfully"}

# Reminder endpoints
@app.get("/reminders", response_model=List[Reminder])
def get_reminders(service: ReminderService = Depends(get_reminder_service)):
    return service.get_all_reminders()

@app.get("/reminders/{reminder_id}", response_model=Reminder)
def get_reminder(reminder_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    reminder = service.get_reminder_by_id(reminder_id)
    if not reminder:
        raise HTTPException(404, "Reminder not found")
    return reminder

@app.get("/tasks/{task_id}/reminders", response_model=List[Reminder])
def get_reminders_by_task(task_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    return service.get_reminders_by_task(task_id)

@app.get("/users/{user_id}/reminders", response_model=List[Reminder])
def get_reminders_by_user(user_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    return service.get_reminders_by_user(user_id)

@app.get("/reminders/pending", response_model=List[Reminder])
def get_pending_reminders(service: ReminderService = Depends(get_reminder_service)):
    return service.get_pending_reminders()

@app.post("/reminders", response_model=Reminder, status_code=201)
def create_reminder(data: ReminderCreate, service: ReminderService = Depends(get_reminder_service)):
    reminder = Reminder(**data.dict())
    return service.create_reminder(reminder)

@app.put("/reminders/{reminder_id}", response_model=Reminder)
def update_reminder(reminder_id: UUID, data: ReminderCreate, service: ReminderService = Depends(get_reminder_service)):
    reminder = Reminder(id=reminder_id, **data.dict())
    updated_reminder = service.update_reminder(reminder)
    if not updated_reminder:
        raise HTTPException(404, "Reminder not found")
    return updated_reminder

@app.delete("/reminders/{reminder_id}")
def delete_reminder(reminder_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    if not service.delete_reminder(reminder_id):
        raise HTTPException(404, "Reminder not found")
    return {"message": "Reminder deleted successfully"}

# Activity Log endpoints
@app.get("/activities", response_model=List[ActivityLog])
def get_activities(service: ActivityLogService = Depends(get_activity_log_service)):
    return service.get_all_activities()

@app.get("/activities/{activity_id}", response_model=ActivityLog)
def get_activity(activity_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    activity = service.get_activity_by_id(activity_id)
    if not activity:
        raise HTTPException(404, "Activity not found")
    return activity

@app.get("/activities/entity/{entity_type}/{entity_id}", response_model=List[ActivityLog])
def get_activities_by_entity(entity_type: str, entity_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    return service.get_activities_by_entity(entity_type, entity_id)

@app.get("/users/{actor_id}/activities", response_model=List[ActivityLog])
def get_activities_by_actor(actor_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    return service.get_activities_by_actor(actor_id)

@app.post("/activities", response_model=ActivityLog, status_code=201)
def create_activity(data: ActivityLogCreate, service: ActivityLogService = Depends(get_activity_log_service)):
    activity = ActivityLog(**data.dict())
    return service.create_activity(activity)

@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    if not service.delete_activity(activity_id):
        raise HTTPException(404, "Activity not found")
    return {"message": "Activity deleted successfully"}