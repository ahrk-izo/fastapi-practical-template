from fastapi import APIRouter, HTTPException, status

from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

tasks: list[TaskResponse] = []
next_task_id = 1


@router.get("", response_model=list[TaskResponse])
def list_tasks() -> list[TaskResponse]:
    """登録されているすべてのタスクを返す。

    Returns:
        タスクのリスト。タスクが存在しない場合は空リストを返す。
    """
    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> TaskResponse:
    """新しいタスクを作成して返す。

    Args:
        task: 作成するタスクのタイトルと説明を含むリクエストボディ。

    Returns:
        作成されたタスク。
    """
    global next_task_id

    new_task = TaskResponse(
        id=next_task_id,
        title=task.title,
        description=task.description,
        completed=False,
    )
    tasks.append(new_task)
    next_task_id += 1

    return new_task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int) -> TaskResponse:
    """指定されたIDのタスクを返す。

    Args:
        task_id: 取得するタスクのID。

    Returns:
        指定されたIDに一致するタスク。

    Raises:
        HTTPException: タスクが存在しない場合は404を返す。
    """
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )
