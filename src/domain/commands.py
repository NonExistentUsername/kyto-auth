from uuid import uuid4

from src.service_player import exceptions


class Command:
    """
    Represents a command that can be executed by the system.

    Attributes:
        id (str): Unique identifier for the command.
    """

    def __init__(self):
        """
        Initializes a new Command instance with a unique identifier.
        """
        self.__id: str = str(uuid4())  # unique id of command

    @property
    def id(self) -> str:
        """
        Get id of command

        Returns:
            str: Command id
        """
        return self.__id


class CreateUser(Command):
    def __init__(self, username: str, email: str, password: str) -> None:
        super().__init__()
        self.username: str = username
        self.email: str = email
        self.password: str = password
