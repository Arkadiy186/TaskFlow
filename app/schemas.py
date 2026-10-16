
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


Role = Literal["operator", "admin"]
TaskStatus = Literal["open", "in_progress", "done"]
TaskPriority = Literal["low", "medium", "high"]


class ReadModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: str = Field(min_length=1, max_length=255)
    display_name: str = Field(min_length=1, max_length=255)
    role: Role = "operator"


class UserUpdate(BaseModel):
    email: str | None = Field(default=None, max_length=255)
    display_name: str | None = Field(default=None, max_length=255)
    role: Role | None = None


class UserRead(ReadModel):
    id: int
    email: str
    display_name: str
    role: str
    created_at: datetime


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None


class ProjectRead(ReadModel):
    id: int
    name: str
    description: str | None
    created_at: datetime


class LabelCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    color: str = "#6b7280"

    @field_validator("color")
    @classmethod
    def validate_color(cls, value: str) -> str:
        import re

        if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            raise ValueError("Color must use #RRGGBB format")
        return value


class LabelUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=64)
    color: str | None = None

    @field_validator("color")
    @classmethod
    def validate_color(cls, value: str | None) -> str | None:
        import re

        if value is not None and not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            raise ValueError("Color must use #RRGGBB format")
        return value


class LabelRead(ReadModel):
    id: int
    name: str
    color: str


class TaskCreate(BaseModel):
    project_id: int
    assignee_id: int | None = None
    label_id: int | None = None
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = "open"
    priority: TaskPriority = "medium"


class TaskUpdate(BaseModel):
    project_id: int | None = None
    assignee_id: int | None = None
    label_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None


class TaskRead(ReadModel):
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


class CommentCreate(BaseModel):
    task_id: int
    author_id: int
    body: str = Field(min_length=1)

    @field_validator("body")
    @classmethod
    def validate_body(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Comment body cannot be empty")
        return value


class CommentUpdate(BaseModel):
    task_id: int | None = None
    author_id: int | None = None
    body: str | None = Field(default=None, min_length=1)

    @field_validator("body")
    @classmethod
    def validate_body(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Comment body cannot be empty")
        return value


class CommentRead(ReadModel):
    id: int
    task_id: int
    author_id: int
    body: str
    created_at: datetime
