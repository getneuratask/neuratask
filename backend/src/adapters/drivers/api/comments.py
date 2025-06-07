"""
Comment endpoints for the NeuralTask API
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from src.domain.schemas import Comment
from src.ports.drivers import CommentService
from .dependencies import get_comment_service
from .dtos import CommentCreateDTO, CommentUpdateDTO

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.get("", response_model=List[Comment])
def get_all_comments(service: CommentService = Depends(get_comment_service)):
    """Get all comments"""
    return service.get_all_comments()

@router.get("/{comment_id}", response_model=Comment)
def get_comment_by_id(comment_id: UUID, service: CommentService = Depends(get_comment_service)):
    """Get comment by ID"""
    comment = service.get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.post("", response_model=Comment, status_code=201)
def create_comment(comment_data: CommentCreateDTO, service: CommentService = Depends(get_comment_service)):
    """Create a new comment"""
    comment = Comment(**comment_data.dict())
    return service.create_comment(comment)

@router.put("/{comment_id}", response_model=Comment)
def update_comment(comment_id: UUID, comment_data: CommentUpdateDTO, service: CommentService = Depends(get_comment_service)):
    """Update comment"""
    existing_comment = service.get_comment_by_id(comment_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    update_data = comment_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_comment, key, value)
    
    updated_comment = service.update_comment(existing_comment)
    if not updated_comment:
        raise HTTPException(status_code=400, detail="Failed to update comment")
    return updated_comment

@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id: UUID, service: CommentService = Depends(get_comment_service)):
    """Delete comment"""
    success = service.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")

# Related endpoints
@router.get("/task/{task_id}", response_model=List[Comment])
def get_comments_by_task(task_id: UUID, service: CommentService = Depends(get_comment_service)):
    """Get comments by task"""
    return service.get_comments_by_task(task_id)

@router.get("/author/{author_id}", response_model=List[Comment])
def get_comments_by_author(author_id: UUID, service: CommentService = Depends(get_comment_service)):
    """Get comments by author"""
    return service.get_comments_by_author(author_id)
