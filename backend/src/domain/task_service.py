from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.task_entity import Task
from src.ports.driven.repository import TaskRepository
from src.ports.drivers.task_service import TaskService


class TaskServiceImpl(TaskService):
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def get_all_tasks(self) -> List[Task]:
        return self.task_repository.get_all()
    
    def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        return self.task_repository.get_by_id(task_id)
    
    def create_task(self, task: Task) -> Task:
        return self.task_repository.create(task)
    
    def update_task(self, task: Task) -> Optional[Task]:
        existing_task = self.task_repository.get_by_id(task.id)
        if not existing_task:
            return None
            
        task.updated_at = datetime.now()
        return self.task_repository.update(task)
    
    def delete_task(self, task_id: UUID) -> bool:
        return self.task_repository.delete(task_id)