from fastapi.testclient import TestClient

from app.main import app
from app.routers import tasks as tasks_router

client = TestClient(app)


def setup_function() -> None:
    tasks_router.tasks.clear()
    tasks_router.next_task_id = 1


def test_list_tasks_returns_empty_list() -> None:
    """タスクが存在しない場合にGET /tasksが空リストを返すことを確認する。

    Returns:
        None
    """
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task_returns_created_task() -> None:
    """POST /tasksが作成されたタスクを返すことを確認する。

    Returns:
        None
    """
    response = client.post(
        "/tasks",
        json={
            "title": "READMEを更新する",
            "description": "タスク管理APIの説明を追加する",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "READMEを更新する",
        "description": "タスク管理APIの説明を追加する",
        "completed": False,
    }


def test_list_tasks_returns_created_tasks() -> None:
    """タスクを作成した後にGET /tasksが作成済みタスクのリストを返すことを確認する。

    Returns:
        None
    """
    client.post(
        "/tasks",
        json={
            "title": "READMEを更新する",
            "description": "タスク管理APIの説明を追加する",
        },
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "READMEを更新する",
            "description": "タスク管理APIの説明を追加する",
            "completed": False,
        }
    ]


def test_get_task_returns_task() -> None:
    """GET /tasks/{task_id}が指定されたIDのタスクを返すことを確認する。

    Returns:
        None
    """
    client.post(
        "/tasks",
        json={
            "title": "READMEを更新する",
            "description": "タスク管理APIの説明を追加する",
        },
    )

    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "READMEを更新する",
        "description": "タスク管理APIの説明を追加する",
        "completed": False,
    }


def test_get_task_returns_404_when_task_does_not_exist() -> None:
    """存在しないタスクIDでGET /tasks/{task_id}を呼び出した場合に404が返ることを確認する。

    Returns:
        None
    """
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "type": "http_error",
            "message": "Task not found",
            "status_code": 404,
        }
    }


def test_create_task_returns_422_when_title_is_missing() -> None:
    """タイトルが欠落したリクエストでPOST /tasksを呼び出した場合に422が返ることを確認する。

    Returns:
        None
    """
    response = client.post(
        "/tasks",
        json={
            "description": "タイトルなし",
        },
    )

    assert response.status_code == 422
