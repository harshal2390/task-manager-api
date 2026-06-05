import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

TOKEN = None
PROJECT_ID = None
TASK_ID = None


def test_1_register_user():

    response = client.post(
        "/auth/register",
        json={
            "email": "harshal@example.com",
            "password": "password123",
            "full_name": "Harshal Chaudhari"
        }
    )

    assert response.status_code in [201, 400]


def test_2_login_user():

    global TOKEN

    response = client.post(
        "/auth/token",
        data={
            "username": "harshal@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data

    TOKEN = data["access_token"]


def test_3_create_project():

    global PROJECT_ID

    response = client.post(
        "/projects",
        headers={
            "Authorization": f"Bearer {TOKEN}"
        },
        json={
            "name": "Pytest Project",
            "description": "Created by pytest"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Pytest Project"

    PROJECT_ID = data["id"]


def test_4_create_task():

    global TASK_ID

    response = client.post(
        f"/projects/{PROJECT_ID}/tasks",
        headers={
            "Authorization": f"Bearer {TOKEN}"
        },
        json={
            "title": "Pytest Task",
            "description": "Task from pytest",
            "priority": 3,
            "status": "todo"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Pytest Task"

    TASK_ID = data["id"]


def test_5_filter_tasks():

    response = client.get(
        f"/projects/{PROJECT_ID}/tasks?status=todo",
        headers={
            "Authorization": f"Bearer {TOKEN}"
        }
    )

    assert response.status_code == 200

    tasks = response.json()

    for task in tasks:
        assert task["status"] == "todo"