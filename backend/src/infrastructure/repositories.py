from typing import Dict, List, Optional
from uuid import UUID

from src.application.ports import TaskRepository
from src.domain.entities import Task


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks: Dict[UUID, Task] = {}
    
    def get_all(self) -> List[Task]:
        return list(self.tasks.values())
    
    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def create(self, task: Task) -> Task:
        self.tasks[task.id] = task
        return task
    
    def update(self, task: Task) -> Optional[Task]:
        if task.id not in self.tasks:
            return None
        
        self.tasks[task.id] = task
        return task
    
    def delete(self, task_id: UUID) -> bool:
        if task_id not in self.tasks:
            return False
        
        del self.tasks[task_id]
        return True