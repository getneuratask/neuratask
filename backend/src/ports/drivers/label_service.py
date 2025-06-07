from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.schemas.label_entity import Label


class LabelService(ABC):
    @abstractmethod
    def get_all_labels(self) -> List[Label]:
        pass

    @abstractmethod
    def get_label_by_id(self, label_id: UUID) -> Optional[Label]:
        pass

    @abstractmethod
    def get_labels_by_workspace(self, workspace_id: UUID) -> List[Label]:
        pass

    @abstractmethod
    def get_labels_by_task(self, task_id: UUID) -> List[Label]:
        pass

    @abstractmethod
    def create_label(self, label: Label) -> Label:
        pass

    @abstractmethod
    def update_label(self, label: Label) -> Optional[Label]:
        pass

    @abstractmethod
    def delete_label(self, label_id: UUID) -> bool:
        pass