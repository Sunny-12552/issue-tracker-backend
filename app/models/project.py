# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from app.db.database import Base


# class Project(Base):
#     __tablename__ = "projects"
    

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     description = Column(String)
#     status = Column(String, default="todo")
#     riority = Column(String, default="medium") # low | medium | high
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     owner = relationship(
#         "User",
#         back_populates="projects"
#     )
#     comments = relationship(
#     "Comment",
#     back_populates="project",
#     cascade="all, delete"
#    )

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="todo")

    # ✅ FIXED HERE
    priority = Column(String, default="medium")  # low | medium | high

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship(
        "User",
        back_populates="projects"
    )

    comments = relationship(
        "Comment",
        back_populates="project",
        cascade="all, delete"
    )
