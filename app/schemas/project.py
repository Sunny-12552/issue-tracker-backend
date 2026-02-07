from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    title: str
    description: str
    priority: Optional[str] = "medium"  # low | medium | high
    status: Optional[str] = "todo"  # todo | in_progress | done


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
