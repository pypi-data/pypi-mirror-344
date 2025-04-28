from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Repository(BaseModel):
    github_id: int
    name: str
    full_name: str
    owner: str
    description: Optional[str] = None
    url: str
    id: str
    user_id: str
    last_scanned: Optional[datetime] = None
    is_active: bool
    custom_prompt: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
