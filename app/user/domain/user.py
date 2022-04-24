from typing import Union, NoReturn, Optional

from sqlalchemy import Column, Unicode, BigInteger, Boolean

from app.user.exception.user import PasswordDoesNotMatchException
from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    password = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False, unique=True)
    nickname = Column(Unicode(255), nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)

    def _is_password_match(self, password1: str, password2: str) -> bool:
        return password1 == password2

    def create(
        self,
        password1: str,
        password2: str,
        email: str,
        nickname: str,
        is_admin: bool = False,
    ) -> Union["User", NoReturn]:
        if not self._is_password_match(password1=password1, password2=password2):
            raise PasswordDoesNotMatchException

        return User(
            password=password1,
            email=email,
            nickname=nickname,
            is_admin=is_admin,
        )

    def change_password(self, password1: str, password2: str) -> Optional[NoReturn]:
        if not self._is_password_match(password1=password1, password2=password2):
            raise PasswordDoesNotMatchException

        self.password = password1
