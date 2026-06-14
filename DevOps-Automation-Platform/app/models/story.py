from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.models.base import Base


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=True)
    completion_month = Column(String(10), nullable=False)
    target_release_month = Column(String(10), nullable=False)
    owner = Column(String(128), nullable=True)
    status = Column(String(50), nullable=False, default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
