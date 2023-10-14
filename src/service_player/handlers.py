import logging
import re
from typing import Callable, Dict

from email_validator import validate_email as validate_email_format

from domain import commands, events, users
from service_player import exceptions, unit_of_work

logger = logging.getLogger(__name__)


def validate_username(username: str) -> None:
    """
    Validate username

    Length must be between 3 and 32 characters

    All characters must be alphanumeric or underscore

    Args:
        username (str): Username to validate
    """

    if not username:
        raise exceptions.InvalidUsername("Username cannot be empty")

    if not 3 <= len(username) <= 32:
        raise exceptions.InvalidUsername(
            f"Username must be between 3 and 32 characters. Username length: {len(username)}"
        )

    regex = r"^[a-zA-Z0-9_]+$"

    if not re.match(regex, username):
        raise exceptions.InvalidUsername(
            f"Username can contain only alphanumeric characters and underscore (^a-zA-Z0-9_+$). Username: {username}"
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

    if not password:
        raise exceptions.InvalidPassword("Password cannot be empty")

    if not 8 <= len(password) <= 32:
        raise exceptions.InvalidPassword(
            f"Password must be between 8 and 32 characters. Password length: {len(password)}"
        )

    if not any(char.isupper() for char in password):
        raise exceptions.InvalidPassword(
            f"Password must contain at least one uppercase letter. Password: {password}"
        )

    if not any(char.islower() for char in password):
        raise exceptions.InvalidPassword(
            f"Password must contain at least one lowercase letter. Password: {password}"
        )

    if not any(char.isdigit() for char in password):
        raise exceptions.InvalidPassword(
            f"Password must contain at least one number. Password: {password}"
        )


def validate_email(email: str) -> None:
    """
    Validate email

    Args:
        email (str): Email to validate
    """

    if not email:
        raise exceptions.InvalidEmail("Email cannot be empty")

    try:
        _ = validate_email_format(email)
    except Exception as e:
        raise exceptions.InvalidEmail(f"Email is not valid. Email: {email}") from e


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

        print(uow.users)

        return user


EVENT_HANDLERS: Dict[events.Event, Callable] = {}
COMMAND_HANDLERS: Dict[commands.Command, Callable] = {
    commands.CreateUser: create_user,
}
