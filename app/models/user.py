from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(String)

    full_name: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    projects = relationship(
        "Project",
        back_populates="owner"
    )

    assigned_tasks = relationship(
        "Task",
        back_populates="assignee"
    )