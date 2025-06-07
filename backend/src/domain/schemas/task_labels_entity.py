from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class TaskLabels:
    """
    Entity representing the many-to-many relationship between tasks and labels.
    This is a junction table that links tasks with their associated labels.
    """
    task_id: UUID
    label_id: UUID

    def __post_init__(self):
        """Validate the entity after initialization."""
        if not isinstance(self.task_id, UUID):
            raise ValueError("task_id must be a valid UUID")
        if not isinstance(self.label_id, UUID):
            raise ValueError("label_id must be a valid UUID")

    def to_dict(self) -> dict:
        """Convert the entity to a dictionary."""
        return {
            "task_id": str(self.task_id),
            "label_id": str(self.label_id)
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TaskLabels":
        """Create a TaskLabels entity from a dictionary."""
        return cls(
            task_id=UUID(data["task_id"]) if isinstance(data["task_id"], str) else data["task_id"],
            label_id=UUID(data["label_id"]) if isinstance(data["label_id"], str) else data["label_id"]
        )

    def __eq__(self, other) -> bool:
        """Check equality based on task_id and label_id."""
        if not isinstance(other, TaskLabels):
            return False
        return self.task_id == other.task_id and self.label_id == other.label_id

    def __hash__(self) -> int:
        """Make the entity hashable for use in sets and as dict keys."""
        return hash((self.task_id, self.label_id))

    def __str__(self) -> str:
        """String representation of the entity."""
        return f"TaskLabels(task_id={self.task_id}, label_id={self.label_id})"

    def __repr__(self) -> str:
        """Detailed string representation for debugging."""
        return self.__str__()