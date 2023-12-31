from kytool.domain.exceptions import InternalException


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


class InvalidPassword(InternalException):
    """
    Raised when password is invalid.
    """

    pass


class UserNotFound(InternalException):
    """
    Raised when user not found.
    """

    pass
