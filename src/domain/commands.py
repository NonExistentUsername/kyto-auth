from kytool.domain.commands import Command


class CreateUser(Command):
    def __init__(self, username: str, email: str, password: str) -> None:
        super().__init__()
        self.username: str = username
        self.email: str = email
        self.password: str = password


class LoginUser(Command):
    def __init__(self, username: str, password: str) -> None:
        super().__init__()
        self.username: str = username
        self.password: str = password
