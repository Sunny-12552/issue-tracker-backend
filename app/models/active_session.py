from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from app.db.database import Base

class ActiveSession(Base):
    __tablename__ = "active_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    login_time = Column(DateTime, default=datetime.utcnow)
