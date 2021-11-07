from typing import Optional, List, Union, NoReturn

from pythondi import inject

from app.users.models import User
from app.users.repositories import UserRepo
from core.db import Transaction, Propagation
from core.exception import CustomException


class UserUsecase:
    @inject()
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo


class GetUserListUsecase(UserUsecase):
    async def execute(self, limit: int, prev: Optional[int]) -> List[User]:
        return await self.user_repo.get_user_list(prev=prev, limit=limit)


class CreateUserUsecase(UserUsecase):
    @Transaction(propagation=Propagation.REQUIRED)
    async def execute(
        self,
        email: str,
        password1: str,
        password2: str,
        nickname: str,
    ) -> Union[User, NoReturn]:
        if password1 != password2:
            raise CustomException(error='password does not match', code=400)

        if await self.user_repo.get_user_by_email_or_nickname(
                email=email,
                nickname=nickname,
        ):
            raise CustomException(error='duplicated email', code=400)

        user = await self.user_repo.create_user(
            email=email,
            password=password1,
            nickname=nickname,
        )
        return user
