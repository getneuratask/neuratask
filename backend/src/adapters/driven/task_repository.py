from typing import Dict, List, Optional
from uuid import UUID

from src.domain.schemas.task_entity import Task
from src.ports.driven.task_repository import TaskRepository
from src.adapters.driven.base_repository import PostgresBaseRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks: Dict[UUID, Task] = {}
    
    def get_all(self) -> List[Task]:
        return list(self.tasks.values())
    
    def get_by_id(self, id: UUID) -> Optional[Task]:
        return self.tasks.get(id)
    
    def create(self, entity: Task) -> Task:
        self.tasks[entity.id] = entity
        return entity
    
    def update(self, entity: Task) -> Optional[Task]:
        if entity.id not in self.tasks:
            return None
        
        self.tasks[entity.id] = entity
        return entity
    
    def delete(self, id: UUID) -> bool:
        if id not in self.tasks:
            return False
        
        del self.tasks[id]
        return True

    def get_by_project_id(self, project_id: UUID) -> List[Task]:
        return [task for task in self.tasks.values() if task.project_id == project_id]

    def get_by_assigned_user(self, user_id: UUID) -> List[Task]:
        return [task for task in self.tasks.values() if task.assigned_to == user_id]

    def get_by_parent_task(self, parent_task_id: UUID) -> List[Task]:
        return [task for task in self.tasks.values() if task.parent_task_id == parent_task_id]


class PostgresTaskRepository(PostgresBaseRepository, TaskRepository):
    def __init__(self, connection_params: dict):
        super().__init__(connection_params)
        self.table = "tasks"

    def get_all(self) -> List[Task]:
        query = f"SELECT * FROM {self.table}"
        results = self._execute_query(query)
        return [Task(**result) for result in results]

    def get_by_id(self, id: UUID) -> Optional[Task]:
        query = f"SELECT * FROM {self.table} WHERE id = %s"
        result = self._execute_single(query, (str(id),))
        return Task(**result) if result else None

    def create(self, entity: Task) -> Task:
        result = self._create_entity(self.table, entity)
        return Task(**result)

    def update(self, entity: Task) -> Optional[Task]:
        result = self._update_entity(self.table, entity)
        return Task(**result) if result else None

    def delete(self, id: UUID) -> bool:
        return self._delete_entity(self.table, id)

    def get_by_project_id(self, project_id: UUID) -> List[Task]:
        query = f"SELECT * FROM {self.table} WHERE project_id = %s"
        results = self._execute_query(query, (str(project_id),))
        return [Task(**result) for result in results]

    def get_by_assigned_user(self, user_id: UUID) -> List[Task]:
        query = f"SELECT * FROM {self.table} WHERE assigned_to = %s"
        results = self._execute_query(query, (str(user_id),))
        return [Task(**result) for result in results]

    def get_by_parent_task(self, parent_task_id: UUID) -> List[Task]:
        query = f"SELECT * FROM {self.table} WHERE parent_task_id = %s"
        results = self._execute_query(query, (str(parent_task_id),))
        return [Task(**result) for result in results]