from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


# Main Task Model (For creating a task)
class Task(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.pending
    due_date: datetime
    class Config:
        from_attributes = True  # Enable ORM mapping for SQLAlchemy models

# Schema for Task Response
class TaskResponse(Task):
    id: UUID  # Unique ID for the task
    created_at: datetime  # The time the task was created
    updated_at: datetime  # The time the task was updated

    class Config:
        from_attributes = True  # Enable ORM mapping for SQLAlchemy models


# Schema for creating a new task
class TaskCreate(Task):
    pass

# Schema for updating an existing task (TaskUpdate)
class TaskUpdate(BaseModel):
    status: TaskStatus
    class Config:
        from_attributes = True  # Enable ORM mapping for SQLAlchemy models
