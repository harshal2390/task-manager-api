from fastapi import FastAPI

# from app.models import (
#     User,
#     Project,
#     Task
# )

from app.api.auth import router as auth_router
from app.api.projects import router as project_router


app = FastAPI(
    title="Task Manager API"
)

app.include_router(auth_router)
app.include_router(project_router)


@app.get("/")
def root():
    return {
        "message": "Task Manager API"
    }