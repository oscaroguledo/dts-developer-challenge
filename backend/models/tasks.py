from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum, Float, Boolean, JSON, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship, validates
from core.database import Base, CHAR_LENGTH
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime, timezone
from enum import Enum as PyEnum
from uuid import uuid4 
from uuid import UUID
from typing import List, Optional
import sys

# Database type detection
if 'postgresql' in sys.argv:
    UUIDType = UUID(as_uuid=True)
    mappeditem = UUID
    default = uuid4
else:
    UUIDType = String(CHAR_LENGTH)
    mappeditem = str
    default = lambda: str(uuid4())

# Enum for task status
class TaskStatus(PyEnum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

# Task Model
class Task(Base):
    __tablename__ = "tasks"

    # Booking ID (UUID as the primary key)
    id: Mapped[UUID] = mapped_column(UUIDType, primary_key=True, default=default)  # UUID with auto-generation
    title: Mapped[str] = mapped_column(String(CHAR_LENGTH), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), nullable=False, default=TaskStatus.pending)
    due_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status})>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }