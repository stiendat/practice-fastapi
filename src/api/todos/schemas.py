from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class TodoCreate(BaseModel):
    """Schema for creating a new todo"""
    title: str = Field(..., description="Title of the todo")


class TodoUpdate(BaseModel):
    """Schema for updating a todo"""
    title: Optional[str] = Field(None, description="Updated title of the todo")
    completed: Optional[bool] = Field(None, description="Updated completion status")


class TodoCreateResponse(BaseModel):
    """Schema for todo creation response"""
    id: str
    title: str
    completed: bool


class TodoListResponse(BaseModel):
    """Schema for todo in list response"""
    id: str
    title: str
    completed: bool
    created_at: str
    updated_at: str


class TodoUpdateResponse(BaseModel):
    """Schema for todo update response"""
    id: str
    title: str
    completed: bool
    updated_at: str


class TodoDeleteResponse(BaseModel):
    """Schema for todo deletion response"""
    message: str
