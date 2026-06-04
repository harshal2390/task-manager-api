from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.project import Project
from app.models.user import User



from app.schemas.task import (TaskCreate,TaskUpdate,TaskResponse)

from app.core.enums import TaskStatus


def create_task(db: Session,project_id: int,task_data: TaskCreate,current_user: User):

    project = (db.query(Project).filter(Project.id == project_id).first())

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Project not found")

    if project.owner_id != current_user.id:raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Access denied")

    task = Task(title=task_data.title,description=task_data.description,
status=task_data.status,
        priority=task_data.priority,
        assignee_id=task_data.assignee_id,
        project_id=project_id,
        due_date=task_data.due_date
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_project_tasks(db: Session,project_id: int,current_user: User,status_filter: TaskStatus | None = None,assignee_id: int | None = None):

    project = (db.query(Project).filter(Project.id == project_id).first())

    if not project:
        raise HTTPException(status_code=404,detail="Project not found")

    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="Access denied")

    query = (db.query(Task).filter(Task.project_id == project_id))

    if status_filter:
        query = query.filter(Task.status == status_filter)

    if assignee_id:
        query = query.filter(Task.assignee_id == assignee_id)

    return query.all()


def update_task(db: Session,task_id: int,task_data: TaskUpdate,current_user: User):

    task = (db.query(Task).filter(Task.id == task_id).first())

    if not task:
        raise HTTPException(status_code=404,detail="Task not found")

    project = (db.query(Project).filter(Project.id == task.project_id).first())

    is_project_owner = (project.owner_id == current_user.id)

    is_assignee = (
        task.assignee_id == current_user.id
    )

    if not (is_project_owner or is_assignee):
        raise HTTPException(status_code=403,detail="Permission denied")

    update_data = (task_data.model_dump(exclude_unset=True))

    for field, value in update_data.items():
        setattr(task,field,value)

    db.commit()

    db.refresh(task)

    return task


def delete_task(db: Session,task_id: int,current_user: User):

    task = (db.query(Task).filter(Task.id == task_id).first())

    if not task:
        raise HTTPException(status_code=404,detail="Task not found")

    project = (db.query(Project).filter(Project.id == task.project_id).first()
    )

    is_project_owner = (project.owner_id == current_user.id)

    is_assignee = (task.assignee_id == current_user.id)

    if not (is_project_owner or is_assignee):
        raise HTTPException(status_code=403,detail="Permission denied")

    db.delete(task)

    db.commit()

    return {
        "message": "Task deleted successfully"
    }
    
    
def update_task_status(db: Session,task_id: int,new_status: TaskStatus,current_user: User):

    task = (db.query(Task).filter(Task.id == task_id).first())

    if not task:
        raise HTTPException(status_code=404,detail="Task not found")

    project = (db.query(Project).filter(Project.id == task.project_id).first())

    is_project_owner = (project.owner_id == current_user.id)

    is_assignee = (task.assignee_id == current_user.id)

    if not (is_project_owner or is_assignee):
        raise HTTPException(status_code=403,detail="Permission denied")

    task.status = new_status

    db.commit()

    db.refresh(task)

    return task