import re
from typing import Optional

from fastapi import APIRouter, status, Response, Cookie
from starlette.exceptions import HTTPException

from memos import store
from memos.schema import UserRequest, ResponseModel

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=ResponseModel)
async def handle_user_sign_up(user_sign_up: UserRequest):
    if not await store.check_username_usable(user_sign_up.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Username `{user_sign_up.username}` already exists")
    user = await store.create_user(user_sign_up.username, user_sign_up.password)
    resp = ResponseModel(
        message=f"Create new user: {user.username}",
        data=user
    )
    return resp


@router.post("/login", response_model=ResponseModel)
async def handle_user_log_in(user_log_in: UserRequest, response: Response):
    try:
        user = await store.get_user_by_username_and_password(user_log_in.username, user_log_in.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    response.set_cookie(key="user_id", value=user.id, expires=3600 * 24 * 30)

    resp = ResponseModel(
        message=f"Welcome, {user.username}!",
        data=user
    )
    return resp


@router.post("/logout")
async def handle_user_log_out(response: Response):
    response.set_cookie(key="user_id", value="", expires=0)
    return {"message": f"Bye."}


@router.get("/user/{username}", response_model=ResponseModel)
async def handle_get_user_by_username(username):
    try:
        user = await store.get_user_by_username(username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])
    resp = ResponseModel(
        message=f"Hi, {user.username}!",
        data=user
    )
    return resp


@router.get("/me", response_model=ResponseModel)
async def handle_get_user_by_username(user_id: Optional[str] = Cookie(default=None)):
    try:
        user = await store.get_user_by_user_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])
    resp = ResponseModel(
        message=f"Welcome, {user.username}!",
        data=user
    )
    return resp
