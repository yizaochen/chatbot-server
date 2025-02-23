from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AssistantBase(BaseModel):
    name: str
    system_prompt: Optional[str] = None
    llm_model_id: int
    user_id: int
    public: bool = False
    activated: bool = True


class AssistantCreate(AssistantBase):
    pass


class AssistantUpdate(BaseModel):
    name: Optional[str] = None
    system_prompt: Optional[str] = None
    llm_model_id: Optional[int] = None
    public: Optional[bool] = None
    activated: Optional[bool] = None


class AssistantResponse(AssistantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
