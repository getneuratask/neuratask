"""
Label endpoints for the NeuralTask API
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from src.domain.schemas import Label
from src.ports.drivers import LabelService
from .dependencies import get_label_service
from .dtos import LabelCreateDTO, LabelUpdateDTO

router = APIRouter(prefix="/labels", tags=["Labels"])

@router.get("", response_model=List[Label])
def get_all_labels(service: LabelService = Depends(get_label_service)):
    """Get all labels"""
    return service.get_all_labels()

@router.get("/{label_id}", response_model=Label)
def get_label_by_id(label_id: UUID, service: LabelService = Depends(get_label_service)):
    """Get label by ID"""
    label = service.get_label_by_id(label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    return label

@router.post("", response_model=Label, status_code=201)
def create_label(label_data: LabelCreateDTO, service: LabelService = Depends(get_label_service)):
    """Create a new label"""
    label = Label(**label_data.dict())
    return service.create_label(label)

@router.put("/{label_id}", response_model=Label)
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

@router.delete("/{label_id}", status_code=204)
def delete_label(label_id: UUID, service: LabelService = Depends(get_label_service)):
    """Delete label"""
    success = service.delete_label(label_id)
    if not success:
        raise HTTPException(status_code=404, detail="Label not found")

# Related endpoints
@router.get("/workspace/{workspace_id}", response_model=List[Label])
def get_labels_by_workspace(workspace_id: UUID, service: LabelService = Depends(get_label_service)):
    """Get labels by workspace"""
    return service.get_labels_by_workspace(workspace_id)

@router.get("/task/{task_id}", response_model=List[Label])
def get_labels_by_task(task_id: UUID, service: LabelService = Depends(get_label_service)):
    """Get labels by task"""
    return service.get_labels_by_task(task_id)
