from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int = None
    password: str = None
    email: str = None
    nickname: str = None
    is_admin: bool = None
    created_at: datetime = None
    updated_at: datetime = None
