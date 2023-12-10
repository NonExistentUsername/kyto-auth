from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kytool.domain.events import Event


class BaseModel:
    """
    Base class for all models in the system.

    Attributes:
        id (str): The unique identifier for the model.
        events (list[Event]): A list of events associated with the model.
    """

    def __init__(self, id: str):
        """
        Initializes a new instance of the Base class.

        Args:
            id (str): The unique identifier for the Base.
        """
        self.__id = id
        self.events: list[Event] = []

    @property
    def id(self) -> str:
        """
        Getter for id

        Returns:
            str: id
        """
        return self.__id
