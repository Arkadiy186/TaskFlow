from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Role = Literal["operator", "admin"]
Status = Literal["open", "in_progress", "done"]
Priority = Literal["low", "medium", "high"]
COLOR = r"^#[0-9a-fA-F]{6}$"


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Read(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(Strict):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=255)
    role: Role = "operator"


class UserUpdate(Strict):
    email: EmailStr = None
    display_name: str = Field(default=None, min_length=1, max_length=255)
    role: Role = None


class UserRead(Read):
    id: int
    email: str
    display_name: str
    role: str
    created_at: datetime


class ProjectCreate(Strict):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None


class ProjectUpdate(Strict):
    name: str = Field(default=None, min_length=1, max_length=200)
    description: str | None = None


class ProjectRead(Read):
    id: int
    name: str
    description: str | None
    created_at: datetime


class LabelCreate(Strict):
    name: str = Field(min_length=1, max_length=64)
    color: str = Field(default="#6b7280", pattern=COLOR)


class LabelUpdate(Strict):
    name: str = Field(default=None, min_length=1, max_length=64)
    color: str = Field(default=None, pattern=COLOR)


class LabelRead(Read):
    id: int
    name: str
    color: str


class TaskCreate(Strict):
    project_id: int
    assignee_id: int | None = None
    label_id: int | None = None
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: Status = "open"
    priority: Priority = "medium"


class TaskUpdate(Strict):
    project_id: int = None
    assignee_id: int | None = None
    label_id: int | None = None
    title: str = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: Status = None
    priority: Priority = None


class TaskRead(Read):
    id: int
    project_id: int
    assignee_id: int | None
    label_id: int | None
    title: str
    description: str | None
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime


class CommentCreate(Strict):
    task_id: int
    author_id: int
    body: str = Field(min_length=1)


class CommentUpdate(Strict):
    task_id: int = None
    author_id: int = None
    body: str = Field(default=None, min_length=1)


class CommentRead(Read):
    id: int
    task_id: int
    author_id: int
    body: str
    created_at: datetime