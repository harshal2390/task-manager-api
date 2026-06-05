from datetime import datetime
from sqlalchemy import String,ForeignKey,DateTime
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.models.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String)

    description: Mapped[str] = mapped_column(String)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)

    owner = relationship("User",back_populates="projects")

    tasks = relationship("Task",back_populates="project",cascade="all, delete-orphan")