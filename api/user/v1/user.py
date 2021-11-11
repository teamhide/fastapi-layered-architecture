from fastapi import APIRouter, Depends

from api.user.v1.request import CreateUserRequest, UpdatePasswordRequest
from api.user.v1.response import CreateUserResponse, GetUserResponse
from app.user.service import UserService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)
from core.fastapi.schemas.response import ExceptionResponseSchema

user_router = APIRouter()


@user_router.post(
    "",
    response_model=CreateUserResponse,
    responses={"400": {"model": ExceptionResponseSchema}},
    summary="Create User",
)
async def create_user(request: CreateUserRequest):
    return await UserService().create_user(**request.dict())


@user_router.get(
    "/{user_id}",
    response_model=GetUserResponse,
    responses={"404": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
    summary="Get User"
)
async def get_user(user_id: int):
    return await UserService().get_user(user_id=user_id)


@user_router.put(
    "/{user_id}/password",
    responses={"404": {"model": ExceptionResponseSchema}},
    summary="Change User Password"
)
async def update_password(request: UpdatePasswordRequest, user_id: int):
    await UserService().update_password(
        user_id=user_id, password1=request.password1, password2=request.password2,
    )
