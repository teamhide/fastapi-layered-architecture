from typing import NoReturn, Union

from pythondi import inject

from app.user.domain import User
from app.user.exception.user import (
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from app.user.repository import UserRepo
from app.user.schema import UserSchema
from core.db import Transactional, Propagation


class UserCommandService:
    @inject()
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_user(
        self, email: str, password1: str, password2: str, nickname: str
    ) -> Union[UserSchema, NoReturn]:
        if await self.user_repo.get_by_email_or_nickname(
            email=email,
            nickname=nickname,
        ):
            raise DuplicateEmailOrNicknameException

        user = User.create(
            password1=password1,
            password2=password2,
            email=email,
            nickname=nickname,
        )
        user = await self.user_repo.save(user=user)
        return UserSchema.from_orm(user)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_password(
        self,
        user_id: int,
        password1: str,
        password2: str,
    ) -> Union[UserSchema, NoReturn]:
        user = await self.user_repo.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException

        user.change_password(password1=password1, password2=password2)
        return UserSchema.from_orm(user)
