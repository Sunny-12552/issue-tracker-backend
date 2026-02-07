from sqlalchemy import Column, Integer
from app.db.database import Base

class AppSettings(Base):
    __tablename__ = "app_settings"

    id = Column(Integer, primary_key=True, index=True)
    max_active_users = Column(Integer, default=1)
