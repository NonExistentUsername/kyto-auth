from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from entrypoints.fastapi_app.responses import Response


def rewrite_404_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Rewrite 404 default exception to custom response

    Args:
        request (Request): Request object
        exc (HTTPException): Exception object

    Returns:
        JSONResponse: Custom response
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=Response(
            message="Not found",
            status_code=status.HTTP_404_NOT_FOUND,
            success=False,
        ).model_dump(),
    )


def rewrite_500_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Rewrite 500 default exception to custom response

    Args:
        request (Request): Request object
        exc (HTTPException): Exception object

    Returns:
        JSONResponse: Custom response
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=Response(
            message="Internal server error",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
        ).model_dump(),
    )
