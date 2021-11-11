from fastapi import APIRouter

from api.user.v1 import sub_router as user_v1_router

router = APIRouter()
router.include_router(user_v1_router)


__all__ = ["router"]
