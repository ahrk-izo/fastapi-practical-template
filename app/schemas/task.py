from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """タスク作成リクエストのスキーマ。"""

    title: str = Field(..., min_length=1)
    description: str | None = None


class TaskResponse(BaseModel):
    """タスクレスポンスのスキーマ。"""

    id: int
    title: str
    description: str | None = None
    completed: bool
