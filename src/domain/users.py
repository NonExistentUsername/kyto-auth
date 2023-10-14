from typing import TYPE_CHECKING, Any

from passlib.hash import argon2

from domain.base import BaseModel

if TYPE_CHECKING:
    from domain.events import Event


class User(BaseModel):
    def __init__(self, id: str, username: str, email: str, password: str) -> None:
        super().__init__(id)
        self.username: str = username
        self.email: str = email
        self._hashed_password: Any = argon2.hash(password)
        self.events: list[Event] = []

    def set_password(self, password: str) -> None:
        self._hashed_password = argon2.hash(password)

    def check_password(self, password: str) -> bool:
        return argon2.verify(password, self._hashed_password)

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
