import logging
import re
from typing import Optional

from kytool.service_player.handlers import register_handler

from src.domain import commands, events, users
from src.service_player import exceptions, unit_of_work

logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_]{3,32}+$")
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,32}$")


def validate_username(username: str) -> None:
    """
    Validate username

    Length must be between 3 and 32 characters

    All characters must be alphanumeric or underscore

    Args:
        username (str): Username to validate
    """

    if not re.match(USERNAME_REGEX, username):
        raise exceptions.InvalidUsername(
            "Username can contain only alphanumeric characters, underscore and must be between 3 and 32 characters."
        )


def validate_password(password: str) -> None:
    """
    Validate password

    Length must be between 8 and 32 characters

    At least one uppercase letter
    At least one lowercase letter
    At least one number

    Args:
        password (str): Password to validate
    """

    if not re.match(PASSWORD_REGEX, password):
        raise exceptions.InvalidPassword(
            "Password must be between 8 and 32 characters and contain at least one uppercase letter, one lowercase letter and one number."
        )


def validate_email(email: str) -> None:
    """
    Validate email

    Args:
        email (str): Email to validate
    """

    if not email:
        raise exceptions.InvalidEmail("Email cannot be empty")

    if not re.match(EMAIL_REGEX, email):
        raise exceptions.InvalidEmail(f"Email is not valid. Email: {email}")


@register_handler(commands.CanCreateUser)
def can_create_user(
    command: commands.CanCreateUser,
    uow: unit_of_work.AbstractUnitOfWork,
) -> bool:
    validate_username(command.username)
    validate_password(command.password)
    validate_email(command.email)

    if uow.users.get(username=command.username):
        raise exceptions.UserAlreadyExists(
            f"User with username {command.username} already exists"
        )

    if uow.users.get(email=command.email):
        raise exceptions.UserAlreadyExists(
            f"User with email {command.email} already exists"
        )

    return True


@register_handler(commands.CreateUser)
def create_user(
    command: commands.CreateUser,
    uow: unit_of_work.AbstractUnitOfWork,
) -> users.User:
    validate_username(command.username)
    validate_password(command.password)
    validate_email(command.email)

    if uow.users.get(username=command.username):
        raise exceptions.UserAlreadyExists(
            f"User with username {command.username} already exists"
        )

    if uow.users.get(email=command.email):
        raise exceptions.UserAlreadyExists(
            f"User with email {command.email} already exists"
        )

    with uow:
        user = users.User(
            id=command.id,
            username=command.username,
            email=command.email,
            password=command.password,
        )

        uow.users.add(user)
        uow.commit()

        return user


@register_handler(commands.LoginUser)
def login_user(
    command: commands.LoginUser,
    uow: unit_of_work.AbstractUnitOfWork,
) -> users.User:
    validate_username(command.username)
    validate_password(command.password)

    with uow:
        user: Optional[users.User] = uow.users.get(username=command.username)  # type: ignore

        if not user:
            raise exceptions.UserNotFound(
                f"User with username {command.username} not found"
            )

        if not user.check_password(command.password):
            raise exceptions.InvalidPassword(
                f"Password is not valid for user with username {command.username}"
            )

        return user
