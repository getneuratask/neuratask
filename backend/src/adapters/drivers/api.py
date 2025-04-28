from typing import List, Optional, Dict, Any
from uuid import UUID
import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr

from src.domain.schemas.task_entity import Task
from src.domain.schemas.user_entity import User
from src.domain.schemas.workspace_entity import Workspace
from src.domain.schemas.project_entity import Project
from src.domain.schemas.label_entity import Label
from src.domain.schemas.comment_entity import Comment
from src.domain.schemas.reminder_entity import Reminder
from src.domain.schemas.activity_log_entity import ActivityLog

from src.domain.task_service import TaskServiceImpl
from src.domain.user_service import UserServiceImpl
from src.domain.workspace_service import WorkspaceServiceImpl
from src.domain.project_service import ProjectServiceImpl
from src.domain.label_service import LabelServiceImpl
from src.domain.comment_service import CommentServiceImpl
from src.domain.reminder_service import ReminderServiceImpl
from src.domain.activity_log_service import ActivityLogServiceImpl

from src.adapters.driven.task_repository import PostgresTaskRepository
from src.adapters.driven.user_repository import PostgresUserRepository
from src.adapters.driven.workspace_repository import PostgresWorkspaceRepository
from src.adapters.driven.project_repository import PostgresProjectRepository
from src.adapters.driven.label_repository import PostgresLabelRepository
from src.adapters.driven.comment_repository import PostgresCommentRepository
from src.adapters.driven.reminder_repository import PostgresReminderRepository
from src.adapters.driven.activity_log_repository import PostgresActivityLogRepository

from src.ports.drivers.task_service import TaskService, UserService, WorkspaceService, ProjectService, LabelService, CommentService, ReminderService, ActivityLogService

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

app = FastAPI(title="NeuralTask API - Hexagonal Architecture")

# DTOs (Data Transfer Objects)
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: UUID
    parent_task_id: Optional[UUID] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class UserCreate(BaseModel):
    auth0_sub: str
    name: str
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None


class WorkspaceCreate(BaseModel):
    name: str
    owner_id: UUID


class ProjectCreate(BaseModel):
    name: str
    workspace_id: UUID
    color: Optional[str] = None


class LabelCreate(BaseModel):
    name: str
    workspace_id: UUID
    color: Optional[str] = None


class CommentCreate(BaseModel):
    body: str
    task_id: UUID
    author_id: UUID


class ReminderCreate(BaseModel):
    task_id: UUID
    user_id: UUID
    remind_at: str
    channel: str


class ActivityLogCreate(BaseModel):
    entity_type: str
    entity_id: UUID
    action: str
    actor_id: UUID
    payload: Optional[Dict[str, Any]] = None


# Dependency Injection
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


# API Endpoints - Tasks
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
    task = Task(title=task_data.title, description=task_data.description, project_id=task_data.project_id, parent_task_id=task_data.parent_task_id)
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


# API Endpoints - Users
@app.get("/users", response_model=List[User])
def get_all_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_all_users()

@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User, status_code=201)
def create_user(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    user = User(**user_data.dict())
    return user_service.create_user(user)

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    user = User(id=user_id, **user_data.dict())
    updated_user = user_service.update_user(user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")


# API Endpoints - Workspaces
@app.get("/workspaces", response_model=List[Workspace])
def get_all_workspaces(workspace_service: WorkspaceService = Depends(get_workspace_service)):
    return workspace_service.get_all_workspaces()

@app.get("/workspaces/{workspace_id}", response_model=Workspace)
def get_workspace_by_id(workspace_id: UUID, workspace_service: WorkspaceService = Depends(get_workspace_service)):
    workspace = workspace_service.get_workspace_by_id(workspace_id)
    if workspace is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@app.get("/users/{user_id}/workspaces", response_model=List[Workspace])
def get_workspaces_by_owner(user_id: UUID, workspace_service: WorkspaceService = Depends(get_workspace_service)):
    return workspace_service.get_workspaces_by_owner(user_id)

@app.post("/workspaces", response_model=Workspace, status_code=201)
def create_workspace(workspace_data: WorkspaceCreate, workspace_service: WorkspaceService = Depends(get_workspace_service)):
    workspace = Workspace(**workspace_data.dict())
    return workspace_service.create_workspace(workspace)

@app.delete("/workspaces/{workspace_id}", status_code=204)
def delete_workspace(workspace_id: UUID, workspace_service: WorkspaceService = Depends(get_workspace_service)):
    success = workspace_service.delete_workspace(workspace_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workspace not found")


# API Endpoints - Projects
@app.get("/projects", response_model=List[Project])
def get_all_projects(project_service: ProjectService = Depends(get_project_service)):
    return project_service.get_all_projects()

@app.get("/projects/{project_id}", response_model=Project)
def get_project_by_id(project_id: UUID, project_service: ProjectService = Depends(get_project_service)):
    project = project_service.get_project_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.get("/workspaces/{workspace_id}/projects", response_model=List[Project])
def get_projects_by_workspace(workspace_id: UUID, project_service: ProjectService = Depends(get_project_service)):
    return project_service.get_projects_by_workspace(workspace_id)

@app.get("/workspaces/{workspace_id}/projects/active", response_model=List[Project])
def get_active_projects_by_workspace(workspace_id: UUID, project_service: ProjectService = Depends(get_project_service)):
    return project_service.get_active_projects_by_workspace(workspace_id)

@app.post("/projects", response_model=Project, status_code=201)
def create_project(project_data: ProjectCreate, project_service: ProjectService = Depends(get_project_service)):
    project = Project(**project_data.dict())
    return project_service.create_project(project)

@app.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: UUID, project_service: ProjectService = Depends(get_project_service)):
    success = project_service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")


# API Endpoints - Labels
@app.get("/labels", response_model=List[Label])
def get_all_labels(label_service: LabelService = Depends(get_label_service)):
    return label_service.get_all_labels()

@app.get("/labels/{label_id}", response_model=Label)
def get_label_by_id(label_id: UUID, label_service: LabelService = Depends(get_label_service)):
    label = label_service.get_label_by_id(label_id)
    if label is None:
        raise HTTPException(status_code=404, detail="Label not found")
    return label

@app.get("/workspaces/{workspace_id}/labels", response_model=List[Label])
def get_labels_by_workspace(workspace_id: UUID, label_service: LabelService = Depends(get_label_service)):
    return label_service.get_labels_by_workspace(workspace_id)

@app.get("/tasks/{task_id}/labels", response_model=List[Label])
def get_labels_by_task(task_id: UUID, label_service: LabelService = Depends(get_label_service)):
    return label_service.get_labels_by_task(task_id)

@app.post("/labels", response_model=Label, status_code=201)
def create_label(label_data: LabelCreate, label_service: LabelService = Depends(get_label_service)):
    label = Label(**label_data.dict())
    return label_service.create_label(label)

@app.delete("/labels/{label_id}", status_code=204)
def delete_label(label_id: UUID, label_service: LabelService = Depends(get_label_service)):
    success = label_service.delete_label(label_id)
    if not success:
        raise HTTPException(status_code=404, detail="Label not found")


# API Endpoints - Comments
@app.get("/comments", response_model=List[Comment])
def get_all_comments(comment_service: CommentService = Depends(get_comment_service)):
    return comment_service.get_all_comments()

@app.get("/comments/{comment_id}", response_model=Comment)
def get_comment_by_id(comment_id: UUID, comment_service: CommentService = Depends(get_comment_service)):
    comment = comment_service.get_comment_by_id(comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@app.get("/tasks/{task_id}/comments", response_model=List[Comment])
def get_comments_by_task(task_id: UUID, comment_service: CommentService = Depends(get_comment_service)):
    return comment_service.get_comments_by_task(task_id)

@app.get("/users/{user_id}/comments", response_model=List[Comment])
def get_comments_by_author(user_id: UUID, comment_service: CommentService = Depends(get_comment_service)):
    return comment_service.get_comments_by_author(user_id)

@app.post("/comments", response_model=Comment, status_code=201)
def create_comment(comment_data: CommentCreate, comment_service: CommentService = Depends(get_comment_service)):
    comment = Comment(**comment_data.dict())
    return comment_service.create_comment(comment)

@app.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: UUID, comment_service: CommentService = Depends(get_comment_service)):
    success = comment_service.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")


# API Endpoints - Reminders
@app.get("/reminders", response_model=List[Reminder])
def get_all_reminders(reminder_service: ReminderService = Depends(get_reminder_service)):
    return reminder_service.get_all_reminders()

@app.get("/reminders/{reminder_id}", response_model=Reminder)
def get_reminder_by_id(reminder_id: UUID, reminder_service: ReminderService = Depends(get_reminder_service)):
    reminder = reminder_service.get_reminder_by_id(reminder_id)
    if reminder is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder

@app.get("/tasks/{task_id}/reminders", response_model=List[Reminder])
def get_reminders_by_task(task_id: UUID, reminder_service: ReminderService = Depends(get_reminder_service)):
    return reminder_service.get_reminders_by_task(task_id)

@app.get("/users/{user_id}/reminders", response_model=List[Reminder])
def get_reminders_by_user(user_id: UUID, reminder_service: ReminderService = Depends(get_reminder_service)):
    return reminder_service.get_reminders_by_user(user_id)

@app.get("/reminders/pending", response_model=List[Reminder])
def get_pending_reminders(reminder_service: ReminderService = Depends(get_reminder_service)):
    return reminder_service.get_pending_reminders()

@app.post("/reminders", response_model=Reminder, status_code=201)
def create_reminder(reminder_data: ReminderCreate, reminder_service: ReminderService = Depends(get_reminder_service)):
    reminder = Reminder(**reminder_data.dict())
    return reminder_service.create_reminder(reminder)

@app.delete("/reminders/{reminder_id}", status_code=204)
def delete_reminder(reminder_id: UUID, reminder_service: ReminderService = Depends(get_reminder_service)):
    success = reminder_service.delete_reminder(reminder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reminder not found")


# API Endpoints - Activity Logs
@app.get("/activities", response_model=List[ActivityLog])
def get_all_activities(activity_service: ActivityLogService = Depends(get_activity_log_service)):
    return activity_service.get_all_activities()

@app.get("/activities/{activity_id}", response_model=ActivityLog)
def get_activity_by_id(activity_id: UUID, activity_service: ActivityLogService = Depends(get_activity_log_service)):
    activity = activity_service.get_activity_by_id(activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@app.get("/activities/entity/{entity_type}/{entity_id}", response_model=List[ActivityLog])
def get_activities_by_entity(
    entity_type: str,
    entity_id: UUID,
    activity_service: ActivityLogService = Depends(get_activity_log_service)
):
    return activity_service.get_activities_by_entity(entity_type, entity_id)

@app.get("/activities/actor/{actor_id}", response_model=List[ActivityLog])
def get_activities_by_actor(actor_id: UUID, activity_service: ActivityLogService = Depends(get_activity_log_service)):
    return activity_service.get_activities_by_actor(actor_id)

@app.post("/activities", response_model=ActivityLog, status_code=201)
def create_activity(activity_data: ActivityLogCreate, activity_service: ActivityLogService = Depends(get_activity_log_service)):
    activity = ActivityLog(**activity_data.dict())
    return activity_service.create_activity(activity)

@app.delete("/activities/{activity_id}", status_code=204)
def delete_activity(activity_id: UUID, activity_service: ActivityLogService = Depends(get_activity_log_service)):
    success = activity_service.delete_activity(activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")