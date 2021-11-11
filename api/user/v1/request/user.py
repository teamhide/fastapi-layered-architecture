from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    email: str
    password1: str
    password2: str
    nickname: str

    class Config:
        schema_extra = {
            "example": {
                "email": "hide@hide.com",
                "password1": "pw",
                "password2": "pw",
                "nickname": "hide",
            }
        }


class UpdatePasswordRequest(BaseModel):
    password1: str
    password2: str

    class Config:
        schema_extra = {
            "example": {
                "password1": "pw",
                "password2": "pw",
            }
        }
