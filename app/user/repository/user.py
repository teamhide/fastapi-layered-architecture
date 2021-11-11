from abc import ABCMeta, abstractmethod
from typing import Optional

from sqlalchemy import or_

from app.user.domain import User
from core.db import session


class UserRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email_or_nickname(
        self, email: str, nickname: str,
    ) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass


class UserMySQLRepo(UserRepo):
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    async def get_by_email_or_nickname(
        self, email: str, nickname: str,
    ) -> Optional[User]:
        return (
            session.query(User)
            .filter(or_(User.email == email, User.nickname == nickname))
            .first()
        )

    async def save(self, user: User) -> User:
        session.add(User)
        return user

    async def delete(self, user: User) -> None:
        session.delete(user)
