from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.label_entity import Label
from src.ports.driven.pg_connection.label_repository import LabelRepository
from src.ports.drivers.label_service import LabelService


class LabelServiceImpl(LabelService):
    def __init__(self, label_repository: LabelRepository):
        self.label_repository = label_repository
    
    def get_all_labels(self) -> List[Label]:
        return self.label_repository.get_all()
    
    def get_label_by_id(self, label_id: UUID) -> Optional[Label]:
        return self.label_repository.get_by_id(label_id)
    
    def get_labels_by_workspace(self, workspace_id: UUID) -> List[Label]:
        return self.label_repository.get_by_workspace(workspace_id)
    
    def get_labels_by_task(self, task_id: UUID) -> List[Label]:
        return self.label_repository.get_by_task(task_id)
    
    def create_label(self, label: Label) -> Label:
        return self.label_repository.create(label)
    
    def update_label(self, label: Label) -> Optional[Label]:
        existing_label = self.label_repository.get_by_id(label.id)
        if not existing_label:
            return None
        return self.label_repository.update(label)
    
    def delete_label(self, label_id: UUID) -> bool:
        return self.label_repository.delete(label_id)