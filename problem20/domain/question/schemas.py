from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class QuestionBase(BaseModel):
    subject: str
    content: str


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    subject: Optional[str] = None
    content: Optional[str] = None


class QuestionRead(QuestionBase):
    id: int
    create_date: datetime

    class Config:
        from_attributes = True