from fastapi import FastAPI


def create_app() -> FastAPI:
    """
    Create FastAPI app
    Application will be created with all routers and exception handlers

    Returns:
        FastAPI: FastAPI app
    """
    import logging

    from auth.entrypoints.fastapi_app.exception_handlers import (
        rewrite_404_exception,
        rewrite_500_exception,
    )
    from auth.entrypoints.fastapi_app.v1.routers import router as api_v1_router

    logging.basicConfig(level=logging.DEBUG)

    app = FastAPI(debug=True)
    app.include_router(api_v1_router)

    app.add_exception_handler(404, rewrite_404_exception)
    app.add_exception_handler(500, rewrite_500_exception)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
