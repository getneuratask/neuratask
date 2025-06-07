"""
NeuralTask API Package - Modular FastAPI implementation
"""

from .main import app, create_app
from .dependencies import (
    get_task_service,
    get_user_service,
    get_workspace_service,
    get_project_service,
    get_label_service,
    get_comment_service,
    get_reminder_service,
    get_activity_log_service
)

# Import all routers for external access if needed
from .users import router as users_router
from .workspaces import router as workspaces_router
from .projects import router as projects_router
from .tasks import router as tasks_router
from .labels import router as labels_router
from .comments import router as comments_router
from .reminders import router as reminders_router
from .activity_logs import router as activity_logs_router

__all__ = [
    # Main app
    "app",
    "create_app",
    
    # Dependency injection functions
    "get_task_service",
    "get_user_service", 
    "get_workspace_service",
    "get_project_service",
    "get_label_service",
    "get_comment_service",
    "get_reminder_service",
    "get_activity_log_service",
    
    # Routers
    "users_router",
    "workspaces_router",
    "projects_router", 
    "tasks_router",
    "labels_router",
    "comments_router",
    "reminders_router",
    "activity_logs_router"
]