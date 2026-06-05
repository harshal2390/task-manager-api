from datetime import date
from datetime import datetime

from sqlalchemy import (String,Integer,ForeignKey,DateTime,Date,Enum)

from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.models.base import Base
from app.core.enums import TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String)

    description: Mapped[str] = mapped_column(String,nullable=True)

    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus),default=TaskStatus.TODO)

    priority: Mapped[int] = mapped_column(Integer)

    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"),nullable=True)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

    due_date: Mapped[date | None] = mapped_column(Date,nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)

    assignee = relationship("User",back_populates="assigned_tasks")

    project = relationship("Project",back_populates="tasks")