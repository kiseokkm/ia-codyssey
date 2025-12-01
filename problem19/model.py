from pydantic import BaseModel

class TodoItem(BaseModel):
    content: str