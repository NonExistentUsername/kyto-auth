class InternalException(Exception):
    """
    Base class for exceptions in this module.
    """

    pass


class UserAlreadyExists(InternalException):
    """
    Raised when user already exists.
    """

    pass


class InvalidUsername(InternalException):
    """
    Raised when username is invalid.
    """

    pass


class InvalidEmail(InternalException):
    """
    Raised when email is invalid.
    """

    pass
