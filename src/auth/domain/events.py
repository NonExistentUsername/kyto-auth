from uuid import uuid4


class Event:
    """
    Represents an event in the system.

    Attributes:
        id (str): The unique identifier of the event.
    """

    def __init__(self):
        """
        Initializes a new Event instance with a unique identifier.
        """
        self.__id: str = str(uuid4())  # unique id of event

    @property
    def id(self) -> str:
        """
        Returns the unique identifier of the event.

        Returns:
            str: The unique identifier of the event.
        """
        return self.__id
