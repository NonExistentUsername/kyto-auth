import logging
import multiprocessing.pool
from typing import Annotated, Union

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from kytool.service_player import messagebus

from src.domain import commands, users
from src.entrypoints.fastapi_app import responses
from src.entrypoints.fastapi_app.deps import get_message_bus
from src.entrypoints.fastapi_app.responses import (
    ErrorResponse,
    InternalErrorResponse,
    Response,
)
from src.entrypoints.fastapi_app.v1 import models
from src.service_player import exceptions

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["main"],
)


@router.post("/register", response_model=Response, status_code=status.HTTP_201_CREATED)
async def register(
    register: models.Register,
    message_bus: Annotated[messagebus.MessageBus, Depends(get_message_bus)],
) -> Union[JSONResponse, Response]:
    """
    Create user endpoint

    It will create user with username, password and email
    """
    try:
        result: bool = message_bus.handle(
            commands.CanCreateUser(
                username=register.username,
                email=register.email,
                password=register.password,
            )
        )
        if result:
            message_bus.handle(
                commands.CreateUser(
                    username=register.username,
                    email=register.email,
                    password=register.password,
                ),
                force_background=True,
            )

        return JSONResponse(
            content=Response(
                message="User created",
                data={},
                status_code=status.HTTP_201_CREATED,
                success=True,
            ).model_dump(),
            status_code=status.HTTP_201_CREATED,
        )
    except exceptions.UserAlreadyExists as e:
        return responses.get_error_respose(
            status_code=status.HTTP_409_CONFLICT,
            exception=e,
        )
    except exceptions.InvalidUsername as e:
        return responses.get_error_respose(
            status_code=status.HTTP_400_BAD_REQUEST,
            exception=e,
        )
    except exceptions.InvalidEmail as e:
        return responses.get_error_respose(
            status_code=status.HTTP_400_BAD_REQUEST,
            exception=e,
        )
    except exceptions.InvalidPassword as e:
        return responses.get_error_respose(
            status_code=status.HTTP_400_BAD_REQUEST,
            exception=e,
        )
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            content=InternalErrorResponse().model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/login", response_model=Response, status_code=status.HTTP_200_OK)
async def login(
    username: str,
    password: str,
    message_bus: Annotated[messagebus.MessageBus, Depends(get_message_bus)],
) -> Union[JSONResponse, Response]:
    """
    Login endpoint

    It will login user with username and password
    """
    try:
        async_result: multiprocessing.pool.ApplyResult = message_bus.handle(
            commands.LoginUser(username=username, password=password)
        )
        user: users.User = async_result.get()

        return JSONResponse(
            content=Response(
                message="User logged in",
                data={
                    "id": user.id,
                    "username": user.username,
                },
                status_code=status.HTTP_200_OK,
                success=True,
            ).model_dump(),
            status_code=status.HTTP_200_OK,
        )
    except exceptions.UserNotFound as e:
        return responses.get_error_respose(
            status_code=status.HTTP_404_NOT_FOUND,
            exception=e,
        )
    except exceptions.InvalidUsername as e:
        return responses.get_error_respose(
            status_code=status.HTTP_400_BAD_REQUEST,
            exception=e,
        )
    except exceptions.InvalidPassword as e:
        return responses.get_error_respose(
            status_code=status.HTTP_400_BAD_REQUEST,
            exception=e,
        )
    except Exception as e:
        logger.exception(e)
        return JSONResponse(
            content=InternalErrorResponse().model_dump(),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
