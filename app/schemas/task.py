from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from app.core.enums import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str | None = None

    status: TaskStatus = TaskStatus.TODO

    priority: int = Field(
        ge=1,
        le=5
    )

    assignee_id: int | None = None

    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None

    priority: int | None = Field(
        default=None,
        ge=1,
        le=5
    )

    assignee_id: int | None = None

    due_date: date | None = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: int
    assignee_id: int | None
    project_id: int
    due_date: date | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }