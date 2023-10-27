import logging
import multiprocessing.pool
from typing import Annotated, Union

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.domain import commands, users
from src.entrypoints.fastapi_app import responses
from src.entrypoints.fastapi_app.deps import get_message_bus
from src.entrypoints.fastapi_app.responses import (
    ErrorResponse,
    InternalErrorResponse,
    Response,
)
from src.service_player import exceptions, messagebus

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def register(
    username: str,
    email: str,
    password: str,
    message_bus: Annotated[messagebus.MessageBus, Depends(get_message_bus)],
) -> Union[JSONResponse, Response]:
    """
    Create user endpoint

    It will create user with username, password and email
    """
    try:
        async_result: multiprocessing.pool.ApplyResult = message_bus.handle(
            commands.CreateUser(username=username, email=email, password=password)
        )
        user: users.User = async_result.get()

        return JSONResponse(
            content=Response(
                message="User created",
                data={
                    "id": user.id,
                    "username": user.username,
                },
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
