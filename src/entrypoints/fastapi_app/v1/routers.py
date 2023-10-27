from fastapi import APIRouter

from src.entrypoints.fastapi_app.v1.endpoints import router as main_router

"""
Here we will include all routers
"""

router = APIRouter(
    prefix="/v1",
)

router.include_router(main_router)
