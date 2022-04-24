from typing import Optional, Union, NoReturn

from pythondi import inject

from app.user.domain import User
from app.user.repository import UserRepo
from core.db import Transactional, Propagation
from core.exceptions.user import (
    UserNotFoundException,
    DuplicateEmailOrNicknameException,
)


class UserService:
    @inject()
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_user(
        self, email: str, password1: str, password2: str, nickname: str
    ) -> Union[User, NoReturn]:
        if await self.user_repo.get_by_email_or_nickname(
            email=email, nickname=nickname
        ):
            raise DuplicateEmailOrNicknameException

        user = User().create(
            password1=password1, password2=password2, email=email, nickname=nickname,
        )
        user = await self.user_repo.save(user=user)
        return user

    async def is_admin(self, user_id: int) -> bool:
        user = await self.user_repo.get_by_id(user_id=user_id)
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

    async def get_user(self, user_id: int) -> Optional[User]:
        user = await self.user_repo.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException

        return user

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_password(
        self, user_id: int, password1: str, password2: str,
    ) -> Union[User, NoReturn]:
        user = await self.user_repo.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException

        user.change_password(password1=password1, password2=password2)
        return user
