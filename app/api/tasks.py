from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from app.core.dependencies import (
    get_db,
    get_current_user
)

from app.models.user import User

from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse
)

from app.core.enums import TaskStatus

from app.services.task_service import (
    create_task,
    get_project_tasks,
    update_task,
    update_task_status,
    delete_task
)


router = APIRouter(
    tags=["Tasks"]
)


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=201
)
def create_project_task(
    project_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return create_task(
        db=db,
        project_id=project_id,
        task_data=task_data,
        current_user=current_user
    )


@router.get(
    "/projects/{project_id}/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    project_id: int,
    status: TaskStatus | None = Query(None),
    assignee_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return get_project_tasks(
        db=db,
        project_id=project_id,
        current_user=current_user,
        status_filter=status,
        assignee_id=assignee_id
    )


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def edit_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return update_task(
        db=db,
        task_id=task_id,
        task_data=task_data,
        current_user=current_user
    )


@router.patch(
    "/tasks/{task_id}/status",
    response_model=TaskResponse
)
def change_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return update_task_status(
        db=db,
        task_id=task_id,
        new_status=status_data.status,
        current_user=current_user
    )


@router.delete(
    "/tasks/{task_id}"
)
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    return delete_task(
        db=db,
        task_id=task_id,
        current_user=current_user
    )