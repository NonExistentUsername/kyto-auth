from typing import Any, Dict

from fastapi.responses import JSONResponse
from pydantic import BaseModel


class Response(BaseModel):
    """
    Basic response model
    """

    status_code: int  # Internal status code
    success: bool
    message: str
    data: Dict[str, Any] = {}


class ErrorResponse(Response):
    """
    Basic response model
    """

    status_code: int  # Internal status code
    success: bool = False
    message: str


class InternalErrorResponse(ErrorResponse):
    """
    Basic response model
    """

    status_code: int = 500  # Internal status code
    message: str = "Internal server error"


def get_error_respose(
    exception: Exception,
    status_code: int = 500,
) -> JSONResponse:
    """
    Get error response

    Args:
        message (str): Error message
        status_code (int, optional): Status code. Defaults to 500.
        success (bool, optional): Success flag. Defaults to False.

    Returns:
        JSONResponse: Error response
    """
    return JSONResponse(
        content=ErrorResponse(
            message=str(exception),
            status_code=status_code,
        ).model_dump(),
        status_code=status_code,
    )
