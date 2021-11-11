from datetime import datetime

from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    id: int
    nickname: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "nickname": "hide",
                "email": "hide@hide.com",
                "created_at": "2021-11-11T07:50:54.289Z",
                "updated_at": "2021-11-11T07:50:54.289Z",
            }
        }


class GetUserResponse(BaseModel):
    id: int
    nickname: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "nickname": "hide",
                "email": "hide@hide.com",
                "created_at": "2021-11-11T07:50:54.289Z",
                "updated_at": "2021-11-11T07:50:54.289Z",
            }
        }

