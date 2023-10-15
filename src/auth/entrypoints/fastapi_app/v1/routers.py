from fastapi import APIRouter

from auth.entrypoints.fastapi_app.v1.users import router as users_router

"""
Here we will include all routers
"""

router = APIRouter(
    prefix="/v1",
)

router.include_router(users_router)
