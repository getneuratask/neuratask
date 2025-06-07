"""
FastAPI application for NeuralTask - Complete API implementation
"""
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

# Domain imports
from src.domain.schemas import (
    Task, TaskStatus, User, Workspace, Project, Label, 
    Comment, Reminder, ReminderChannel, ActivityLog
)
from src.domain import (
    TaskServiceImpl, UserServiceImpl, WorkspaceServiceImpl,
    ProjectServiceImpl, LabelServiceImpl, CommentServiceImpl,
    ReminderServiceImpl, ActivityLogServiceImpl
)

# Repository imports
from src.adapters.driven.pg_repository.task_repository import PostgresTaskRepository
from src.adapters.driven.pg_repository.user_repository import PostgresUserRepository
from src.adapters.driven.pg_repository.workspace_repository import PostgresWorkspaceRepository
from src.adapters.driven.pg_repository.project_repository import PostgresProjectRepository
from src.adapters.driven.pg_repository.label_repository import PostgresLabelRepository
from src.adapters.driven.pg_repository.comment_repository import PostgresCommentRepository
from src.adapters.driven.pg_repository.reminder_repository import PostgresReminderRepository
from src.adapters.driven.pg_repository.activity_log_repository import PostgresActivityLogRepository

# Service ports imports
from src.ports.drivers import (
    TaskService, UserService, WorkspaceService, ProjectService,
    LabelService, CommentService, ReminderService, ActivityLogService
)

# Database configuration
DB_PARAMS = {
    "host": "localhost",
    "port": 5432,
    "database": "neuratask",
    "user": "postgres",
    "password": "postgres"
}

# FastAPI app initialization
app = FastAPI(
    title="NeuralTask API",
    description="Complete task management system API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# DTOs (Data Transfer Objects) for API requests
# =====================================================

class TaskCreateDTO(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: UUID
    parent_task_id: Optional[UUID] = None
    priority: int = 4
    due_date: Optional[date] = None
    start_date: Optional[date] = None
    assigned_to: Optional[UUID] = None
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None

class TaskUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = None
    due_date: Optional[date] = None
    start_date: Optional[date] = None
    assigned_to: Optional[UUID] = None
    is_recurring: Optional[bool] = None
    recurrence_rule: Optional[str] = None

class UserCreateDTO(BaseModel):
    auth0_sub: str
    name: str
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None

class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None

class WorkspaceCreateDTO(BaseModel):
    name: str
    owner_id: UUID

class WorkspaceUpdateDTO(BaseModel):
    name: Optional[str] = None

class ProjectCreateDTO(BaseModel):
    name: str
    workspace_id: UUID
    color: Optional[str] = None
    sort_order: int = 0

class ProjectUpdateDTO(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    sort_order: Optional[int] = None
    is_archived: Optional[bool] = None

class LabelCreateDTO(BaseModel):
    name: str
    workspace_id: UUID
    color: Optional[str] = None

class LabelUpdateDTO(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None

class CommentCreateDTO(BaseModel):
    task_id: UUID
    author_id: UUID
    body: str

class CommentUpdateDTO(BaseModel):
    body: str

class ReminderCreateDTO(BaseModel):
    task_id: UUID
    user_id: UUID
    remind_at: datetime
    channel: ReminderChannel = ReminderChannel.PUSH

class ReminderUpdateDTO(BaseModel):
    remind_at: Optional[datetime] = None
    channel: Optional[ReminderChannel] = None

class ActivityLogCreateDTO(BaseModel):
    entity_type: str
    entity_id: UUID
    action: str
    actor_id: UUID
    payload: Optional[Dict[str, Any]] = None

# =====================================================
# Dependency Injection
# =====================================================

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

# =====================================================
# Health Check
# =====================================================

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

# =====================================================
# USER ENDPOINTS
# =====================================================

@app.get("/users", response_model=List[User], tags=["Users"])
def get_all_users(service: UserService = Depends(get_user_service)):
    """Get all users"""
    return service.get_all_users()

@app.get("/users/{user_id}", response_model=User, tags=["Users"])
def get_user_by_id(user_id: UUID, service: UserService = Depends(get_user_service)):
    """Get user by ID"""
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/auth0/{auth0_sub}", response_model=User, tags=["Users"])
def get_user_by_auth0_sub(auth0_sub: str, service: UserService = Depends(get_user_service)):
    """Get user by Auth0 subject"""
    user = service.get_user_by_auth0_sub(auth0_sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/email/{email}", response_model=User, tags=["Users"])
def get_user_by_email(email: str, service: UserService = Depends(get_user_service)):
    """Get user by email"""
    user = service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User, status_code=201, tags=["Users"])
def create_user(user_data: UserCreateDTO, service: UserService = Depends(get_user_service)):
    """Create a new user"""
    user = User(**user_data.dict())
    return service.create_user(user)

@app.put("/users/{user_id}", response_model=User, tags=["Users"])
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

@app.delete("/users/{user_id}", status_code=204, tags=["Users"])
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    """Delete user"""
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

# =====================================================
# WORKSPACE ENDPOINTS
# =====================================================

@app.get("/workspaces", response_model=List[Workspace], tags=["Workspaces"])
def get_all_workspaces(service: WorkspaceService = Depends(get_workspace_service)):
    """Get all workspaces"""
    return service.get_all_workspaces()

@app.get("/workspaces/{workspace_id}", response_model=Workspace, tags=["Workspaces"])
def get_workspace_by_id(workspace_id: UUID, service: WorkspaceService = Depends(get_workspace_service)):
    """Get workspace by ID"""
    workspace = service.get_workspace_by_id(workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@app.get("/users/{owner_id}/workspaces", response_model=List[Workspace], tags=["Workspaces"])
def get_workspaces_by_owner(owner_id: UUID, service: WorkspaceService = Depends(get_workspace_service)):
    """Get workspaces by owner"""
    return service.get_workspaces_by_owner(owner_id)

@app.post("/workspaces", response_model=Workspace, status_code=201, tags=["Workspaces"])
def create_workspace(workspace_data: WorkspaceCreateDTO, service: WorkspaceService = Depends(get_workspace_service)):
    """Create a new workspace"""
    workspace = Workspace(**workspace_data.dict())
    return service.create_workspace(workspace)

@app.put("/workspaces/{workspace_id}", response_model=Workspace, tags=["Workspaces"])
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

@app.delete("/workspaces/{workspace_id}", status_code=204, tags=["Workspaces"])
def delete_workspace(workspace_id: UUID, service: WorkspaceService = Depends(get_workspace_service)):
    """Delete workspace"""
    success = service.delete_workspace(workspace_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workspace not found")

# =====================================================
# PROJECT ENDPOINTS
# =====================================================

@app.get("/projects", response_model=List[Project], tags=["Projects"])
def get_all_projects(service: ProjectService = Depends(get_project_service)):
    """Get all projects"""
    return service.get_all_projects()

@app.get("/projects/{project_id}", response_model=Project, tags=["Projects"])
def get_project_by_id(project_id: UUID, service: ProjectService = Depends(get_project_service)):
    """Get project by ID"""
    project = service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.get("/workspaces/{workspace_id}/projects", response_model=List[Project], tags=["Projects"])
def get_projects_by_workspace(workspace_id: UUID, service: ProjectService = Depends(get_project_service)):
    """Get projects by workspace"""
    return service.get_projects_by_workspace(workspace_id)

@app.get("/workspaces/{workspace_id}/projects/active", response_model=List[Project], tags=["Projects"])
def get_active_projects_by_workspace(workspace_id: UUID, service: ProjectService = Depends(get_project_service)):
    """Get active projects by workspace"""
    return service.get_active_projects_by_workspace(workspace_id)

@app.post("/projects", response_model=Project, status_code=201, tags=["Projects"])
def create_project(project_data: ProjectCreateDTO, service: ProjectService = Depends(get_project_service)):
    """Create a new project"""
    project = Project(**project_data.dict())
    return service.create_project(project)

@app.put("/projects/{project_id}", response_model=Project, tags=["Projects"])
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

@app.delete("/projects/{project_id}", status_code=204, tags=["Projects"])
def delete_project(project_id: UUID, service: ProjectService = Depends(get_project_service)):
    """Delete project"""
    success = service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")

# =====================================================
# TASK ENDPOINTS
# =====================================================

@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
def get_all_tasks(service: TaskService = Depends(get_task_service)):
    """Get all tasks"""
    return service.get_all_tasks()

@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def get_task_by_id(task_id: UUID, service: TaskService = Depends(get_task_service)):
    """Get task by ID"""
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/projects/{project_id}/tasks", response_model=List[Task], tags=["Tasks"])
def get_tasks_by_project(project_id: UUID, service: TaskService = Depends(get_task_service)):
    """Get tasks by project"""
    return service.get_tasks_by_project(project_id)

@app.get("/users/{user_id}/tasks", response_model=List[Task], tags=["Tasks"])
def get_tasks_by_assigned_user(user_id: UUID, service: TaskService = Depends(get_task_service)):
    """Get tasks assigned to user"""
    return service.get_tasks_by_assigned_user(user_id)

@app.get("/tasks/{parent_task_id}/subtasks", response_model=List[Task], tags=["Tasks"])
def get_subtasks(parent_task_id: UUID, service: TaskService = Depends(get_task_service)):
    """Get subtasks of a task"""
    return service.get_subtasks(parent_task_id)

@app.post("/tasks", response_model=Task, status_code=201, tags=["Tasks"])
def create_task(task_data: TaskCreateDTO, created_by: UUID, service: TaskService = Depends(get_task_service)):
    """Create a new task"""
    task_dict = task_data.dict()
    task_dict['created_by'] = created_by
    task = Task(**task_dict)
    return service.create_task(task)

@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
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

@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
def delete_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    """Delete task"""
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

# =====================================================
# LABEL ENDPOINTS
# =====================================================

@app.get("/labels", response_model=List[Label], tags=["Labels"])
def get_all_labels(service: LabelService = Depends(get_label_service)):
    """Get all labels"""
    return service.get_all_labels()

@app.get("/labels/{label_id}", response_model=Label, tags=["Labels"])
def get_label_by_id(label_id: UUID, service: LabelService = Depends(get_label_service)):
    """Get label by ID"""
    label = service.get_label_by_id(label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    return label

@app.get("/workspaces/{workspace_id}/labels", response_model=List[Label], tags=["Labels"])
def get_labels_by_workspace(workspace_id: UUID, service: LabelService = Depends(get_label_service)):
    """Get labels by workspace"""
    return service.get_labels_by_workspace(workspace_id)

@app.get("/tasks/{task_id}/labels", response_model=List[Label], tags=["Labels"])
def get_labels_by_task(task_id: UUID, service: LabelService = Depends(get_label_service)):
    """Get labels by task"""
    return service.get_labels_by_task(task_id)

@app.post("/labels", response_model=Label, status_code=201, tags=["Labels"])
def create_label(label_data: LabelCreateDTO, service: LabelService = Depends(get_label_service)):
    """Create a new label"""
    label = Label(**label_data.dict())
    return service.create_label(label)

@app.put("/labels/{label_id}", response_model=Label, tags=["Labels"])
def update_label(label_id: UUID, label_data: LabelUpdateDTO, service: LabelService = Depends(get_label_service)):
    """Update label"""
    existing_label = service.get_label_by_id(label_id)
    if not existing_label:
        raise HTTPException(status_code=404, detail="Label not found")
    
    update_data = label_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_label, key, value)
    
    updated_label = service.update_label(existing_label)
    if not updated_label:
        raise HTTPException(status_code=400, detail="Failed to update label")
    return updated_label

@app.delete("/labels/{label_id}", status_code=204, tags=["Labels"])
def delete_label(label_id: UUID, service: LabelService = Depends(get_label_service)):
    """Delete label"""
    success = service.delete_label(label_id)
    if not success:
        raise HTTPException(status_code=404, detail="Label not found")

# =====================================================
# COMMENT ENDPOINTS
# =====================================================

@app.get("/comments", response_model=List[Comment], tags=["Comments"])
def get_all_comments(service: CommentService = Depends(get_comment_service)):
    """Get all comments"""
    return service.get_all_comments()

@app.get("/comments/{comment_id}", response_model=Comment, tags=["Comments"])
def get_comment_by_id(comment_id: UUID, service: CommentService = Depends(get_comment_service)):
    """Get comment by ID"""
    comment = service.get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@app.get("/tasks/{task_id}/comments", response_model=List[Comment], tags=["Comments"])
def get_comments_by_task(task_id: UUID, service: CommentService = Depends(get_comment_service)):
    """Get comments by task"""
    return service.get_comments_by_task(task_id)

@app.get("/users/{author_id}/comments", response_model=List[Comment], tags=["Comments"])
def get_comments_by_author(author_id: UUID, service: CommentService = Depends(get_comment_service)):
    """Get comments by author"""
    return service.get_comments_by_author(author_id)

@app.post("/comments", response_model=Comment, status_code=201, tags=["Comments"])
def create_comment(comment_data: CommentCreateDTO, service: CommentService = Depends(get_comment_service)):
    """Create a new comment"""
    comment = Comment(**comment_data.dict())
    return service.create_comment(comment)

@app.put("/comments/{comment_id}", response_model=Comment, tags=["Comments"])
def update_comment(comment_id: UUID, comment_data: CommentUpdateDTO, service: CommentService = Depends(get_comment_service)):
    """Update comment"""
    existing_comment = service.get_comment_by_id(comment_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    update_data = comment_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_comment, key, value)
    
    updated_comment = service.update_comment(existing_comment)
    if not updated_comment:
        raise HTTPException(status_code=400, detail="Failed to update comment")
    return updated_comment

@app.delete("/comments/{comment_id}", status_code=204, tags=["Comments"])
def delete_comment(comment_id: UUID, service: CommentService = Depends(get_comment_service)):
    """Delete comment"""
    success = service.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")

# =====================================================
# REMINDER ENDPOINTS
# =====================================================

@app.get("/reminders", response_model=List[Reminder], tags=["Reminders"])
def get_all_reminders(service: ReminderService = Depends(get_reminder_service)):
    """Get all reminders"""
    return service.get_all_reminders()

@app.get("/reminders/{reminder_id}", response_model=Reminder, tags=["Reminders"])
def get_reminder_by_id(reminder_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    """Get reminder by ID"""
    reminder = service.get_reminder_by_id(reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder

@app.get("/tasks/{task_id}/reminders", response_model=List[Reminder], tags=["Reminders"])
def get_reminders_by_task(task_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    """Get reminders by task"""
    return service.get_reminders_by_task(task_id)

@app.get("/users/{user_id}/reminders", response_model=List[Reminder], tags=["Reminders"])
def get_reminders_by_user(user_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    """Get reminders by user"""
    return service.get_reminders_by_user(user_id)

@app.get("/reminders/pending", response_model=List[Reminder], tags=["Reminders"])
def get_pending_reminders(service: ReminderService = Depends(get_reminder_service)):
    """Get pending reminders"""
    return service.get_pending_reminders()

@app.post("/reminders", response_model=Reminder, status_code=201, tags=["Reminders"])
def create_reminder(reminder_data: ReminderCreateDTO, service: ReminderService = Depends(get_reminder_service)):
    """Create a new reminder"""
    reminder = Reminder(**reminder_data.dict())
    return service.create_reminder(reminder)

@app.put("/reminders/{reminder_id}", response_model=Reminder, tags=["Reminders"])
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

@app.delete("/reminders/{reminder_id}", status_code=204, tags=["Reminders"])
def delete_reminder(reminder_id: UUID, service: ReminderService = Depends(get_reminder_service)):
    """Delete reminder"""
    success = service.delete_reminder(reminder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reminder not found")

# =====================================================
# ACTIVITY LOG ENDPOINTS
# =====================================================

@app.get("/activity-logs", response_model=List[ActivityLog], tags=["Activity Logs"])
def get_all_activities(service: ActivityLogService = Depends(get_activity_log_service)):
    """Get all activity logs"""
    return service.get_all_activities()

@app.get("/activity-logs/{activity_id}", response_model=ActivityLog, tags=["Activity Logs"])
def get_activity_by_id(activity_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    """Get activity log by ID"""
    activity = service.get_activity_by_id(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity log not found")
    return activity

@app.get("/activity-logs/entity/{entity_type}/{entity_id}", response_model=List[ActivityLog], tags=["Activity Logs"])
def get_activities_by_entity(entity_type: str, entity_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    """Get activity logs by entity"""
    return service.get_activities_by_entity(entity_type, entity_id)

@app.get("/users/{actor_id}/activity-logs", response_model=List[ActivityLog], tags=["Activity Logs"])
def get_activities_by_actor(actor_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    """Get activity logs by actor"""
    return service.get_activities_by_actor(actor_id)

@app.post("/activity-logs", response_model=ActivityLog, status_code=201, tags=["Activity Logs"])
def create_activity(activity_data: ActivityLogCreateDTO, service: ActivityLogService = Depends(get_activity_log_service)):
    """Create a new activity log entry"""
    activity = ActivityLog(**activity_data.dict())
    return service.create_activity(activity)

@app.delete("/activity-logs/{activity_id}", status_code=204, tags=["Activity Logs"])
def delete_activity(activity_id: UUID, service: ActivityLogService = Depends(get_activity_log_service)):
    """Delete activity log"""
    success = service.delete_activity(activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity log not found")

# =====================================================
# UTILITY ENDPOINTS
# =====================================================

@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to NeuralTask API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
