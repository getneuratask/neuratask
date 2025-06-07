from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.project_entity import Project
from src.ports.driven.pg_connection.project_repository import ProjectRepository
from src.ports.drivers.project_service import ProjectService


class ProjectServiceImpl(ProjectService):
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository
    
    def get_all_projects(self) -> List[Project]:
        return self.project_repository.get_all()
    
    def get_project_by_id(self, project_id: UUID) -> Optional[Project]:
        return self.project_repository.get_by_id(project_id)
    
    def get_projects_by_workspace(self, workspace_id: UUID) -> List[Project]:
        return self.project_repository.get_by_workspace(workspace_id)
    
    def get_active_projects_by_workspace(self, workspace_id: UUID) -> List[Project]:
        return self.project_repository.get_active_by_workspace(workspace_id)
    
    def create_project(self, project: Project) -> Project:
        return self.project_repository.create(project)
    
    def update_project(self, project: Project) -> Optional[Project]:
        existing_project = self.project_repository.get_by_id(project.id)
        if not existing_project:
            return None
            
        project.updated_at = datetime.now()
        return self.project_repository.update(project)
    
    def delete_project(self, project_id: UUID) -> bool:
        return self.project_repository.delete(project_id)