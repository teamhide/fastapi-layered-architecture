from fastapi import APIRouter

from .user import user_router

sub_router = APIRouter()
sub_router.include_router(user_router, prefix="/api/v1/users", tags=["User"])


__all__ = ["sub_router"]
