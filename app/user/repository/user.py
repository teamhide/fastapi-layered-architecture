from abc import ABCMeta, abstractmethod
from typing import Optional, List

from sqlalchemy import or_, select

from app.user.domain import User
from core.db import session


class UserRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email_or_nickname(
        self,
        email: str,
        nickname: str,
    ) -> Optional[User]:
        pass

    @abstractmethod
    async def get_users(self) -> List[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass


class UserMySQLRepo(UserRepo):
    async def get_by_id(self, user_id: int) -> Optional[User]:
        return await session.get(User, user_id)

    async def get_by_email_or_nickname(
        self,
        email: str,
        nickname: str,
    ) -> Optional[User]:
        query = await session.execute(
            select(User).where(or_(User.email == email, User.nickname == nickname))
        )

        return query.scalars().first()

    async def get_users(self) -> List[User]:
        query = await session.execute(select(User))
        return query.scalars().all()

    async def save(self, user: User) -> User:
        session.add(user)
        return user

    async def delete(self, user: User) -> None:
        await session.delete(user)
