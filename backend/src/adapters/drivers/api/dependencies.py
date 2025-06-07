"""
Dependency injection for services
"""
import os
from dotenv import load_dotenv
from src.domain import (
    TaskServiceImpl, UserServiceImpl, WorkspaceServiceImpl,
    ProjectServiceImpl, LabelServiceImpl, CommentServiceImpl,
    ReminderServiceImpl, ActivityLogServiceImpl
)
from src.adapters.driven.pg_repository.task_repository import PostgresTaskRepository
from src.adapters.driven.pg_repository.user_repository import PostgresUserRepository
from src.adapters.driven.pg_repository.workspace_repository import PostgresWorkspaceRepository
from src.adapters.driven.pg_repository.project_repository import PostgresProjectRepository
from src.adapters.driven.pg_repository.label_repository import PostgresLabelRepository
from src.adapters.driven.pg_repository.comment_repository import PostgresCommentRepository
from src.adapters.driven.pg_repository.reminder_repository import PostgresReminderRepository
from src.adapters.driven.pg_repository.activity_log_repository import PostgresActivityLogRepository
from src.ports.drivers import (
    TaskService, UserService, WorkspaceService, ProjectService,
    LabelService, CommentService, ReminderService, ActivityLogService
)

# Load environment variables
load_dotenv()

# Database configuration
DB_PARAMS = {
    "host": os.getenv("NEON_TECH_DB_HOST"),
    "port": int(os.getenv("NEON_TECH_DB_PORT", 5432)),
    "database": os.getenv("NEON_TECH_DB_NAME"),
    "user": os.getenv("NEON_TECH_DB_USER"),
    "password": os.getenv("npg_tlf9uaUEKy3P")
}

# =====================================================
# Service Dependencies
# =====================================================

def get_task_service() -> TaskService:
    repository = PostgresTaskRepository()
    return TaskServiceImpl(repository)

def get_user_service() -> UserService:
    repository = PostgresUserRepository()
    return UserServiceImpl(repository)

def get_workspace_service() -> WorkspaceService:
    repository = PostgresWorkspaceRepository()
    return WorkspaceServiceImpl(repository)

def get_project_service() -> ProjectService:
    repository = PostgresProjectRepository()
    return ProjectServiceImpl(repository)

def get_label_service() -> LabelService:
    repository = PostgresLabelRepository()
    return LabelServiceImpl(repository)

def get_comment_service() -> CommentService:
    repository = PostgresCommentRepository()
    return CommentServiceImpl(repository)

def get_reminder_service() -> ReminderService:
    repository = PostgresReminderRepository()
    return ReminderServiceImpl(repository)

def get_activity_log_service() -> ActivityLogService:
    repository = PostgresActivityLogRepository()
    return ActivityLogServiceImpl(repository)
