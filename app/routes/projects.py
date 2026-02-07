from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.project import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])

VALID_STATUSES = {"todo", "in_progress", "done"}


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Project)
        .filter(Project.owner_id == current_user.id)
        .all()
    )


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project_by_id(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.post(
    "/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED
)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ✅ SAFE STATUS VALIDATION
    if project.status and project.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid status value",
        )

    new_project = Project(
        title=project.title,
        description=project.description,
        status=project.status or "todo",
        owner_id=current_user.id,
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 🔐 OWNER AUTHORIZATION
    db_project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if not db_project:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to edit this ticket"
        )

    # ✅ STATUS VALIDATION
    if project.status and project.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid status value",
        )

    if project.title is not None:
        db_project.title = project.title
    if project.description is not None:
        db_project.description = project.description
    if project.status is not None:
        db_project.status = project.status

    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 🔐 OWNER AUTHORIZATION
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == current_user.id,
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this ticket"
        )

    # 🚫 BUSINESS RULE: DELETE ONLY AFTER DONE
    if project.status != "done":
        raise HTTPException(
            status_code=400,
            detail="Ticket must be in Done status before deletion"
        )

    db.delete(project)
    db.commit()
    return None
