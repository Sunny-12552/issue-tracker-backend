from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.comment import Comment
from app.models.project import Project
from app.schemas.comment import CommentCreate, CommentResponse
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/{project_id}", response_model=CommentResponse)
def add_comment(
    project_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Ticket not found")

    comment = Comment(
        content=data.content,
        project_id=project_id,
        user_id=current_user.id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/{project_id}", response_model=list[CommentResponse])
def get_comments(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Comment).filter(
        Comment.project_id == project_id
    ).order_by(Comment.created_at).all()
