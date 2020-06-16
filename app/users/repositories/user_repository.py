from abc import ABCMeta, abstractmethod
from typing import Optional, List, Union, NoReturn

from sqlalchemy import or_

from app.users.models import User
from core.db import session
from core.exception import CustomException


class UserRepo:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email_or_nickname(
        self,
        email: str,
        nickname: str,
    ) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_list(self, prev: int = None, limit: int = None) -> List[User]:
        pass

    @abstractmethod
    def create_user(self, email: str, password: str, nickname: str) -> User:
        pass

    @abstractmethod
    def update_user(
        self,
        user_id: int = None,
        password: str = None,
        email: str = None,
        nickname: str = None,
    ) -> Union[User, NoReturn]:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass


class UserMySQLRepo(UserRepo):
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return session.query(User).get(user_id)

    def get_user_by_email_or_nickname(
        self,
        email: str,
        nickname: str,
    ) -> Optional[User]:
        return session.query(User).filter(
            or_(
                User.email == email,
                User.nickname == nickname,
            ),
        ).first()

    def get_user_list(self, prev: int = None, limit: int = None) -> List[User]:
        query = session.query(User)

        if prev:
            query = query.filter(User.id < prev)

        if limit:
            query = query.limit(limit)

        return query.order_by(User.id.desc()).all()

    def create_user(self, email: str, password: str, nickname: str) -> User:
        user = User(email=email, password=password, nickname=nickname)
        session.add(user)
        return user

    def update_user(
        self,
        user_id: int = None,
        password: str = None,
        email: str = None,
        nickname: str = None,
    ) -> Union[User, NoReturn]:
        user = session.query(User).get(user_id)

        if not user:
            raise CustomException(error='user does not exist', code=500)

        if password:
            user.password = password

        if email:
            user.email = email

        if nickname:
            user.nickname = nickname

        session.add(user)
        return user

    def delete_user(self, user_id: int) -> None:
        user = session.query(User).get(user_id)

        if not user:
            raise CustomException(error='user does not exist', code=500)

        user.delete()
