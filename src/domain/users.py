from typing import TYPE_CHECKING, Any

import bcrypt

from src.domain.base import BaseModel

if TYPE_CHECKING:
    from src.domain.events import Event


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


class User(BaseModel):
    def __init__(self, id: str, username: str, email: str, password: str) -> None:
        super().__init__(id)
        self.username: str = username
        self.email: str = email
        self._hashed_password: Any = _hash_password(password)
        self.events: list[Event] = []

    def set_password(self, password: str) -> None:
        self._hashed_password = _hash_password(password)

    def check_password(self, password: str) -> bool:
        return _check_password(password, self._hashed_password)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False

        return (
            self.id == other.id
            and self.username == other.username
            and self._hashed_password == other._hashed_password
        )

    def __hash__(self) -> int:
        return hash(self.id)
