from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User

from app.schemas.project import ProjectCreate


def create_project(
    db: Session,
    project_data: ProjectCreate,
    current_user: User
):

    project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id
    )

    db.add(project)

    db.commit()

    db.refresh(project)

    return project


def get_user_projects(
    db: Session,
    current_user: User
):

    projects = (
        db.query(Project)
        .filter(
            Project.owner_id == current_user.id
        )
        .all()
    )

    return projects