from fastapi import APIRouter

from api.user.v1.user import user_router

sub_router = APIRouter()
sub_router.include_router(user_router, prefix="/users", tags=["User"])


__all__ = ["sub_router"]
