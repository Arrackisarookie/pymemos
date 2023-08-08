from fastapi import APIRouter, status, Request
from starlette.exceptions import HTTPException

from memos.auth import service
from memos.auth.schemas import UserRequest
from memos.schemas import ResponseModel

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=ResponseModel)
async def handle_user_sign_up(user_sign_up: UserRequest, request: Request):
    if not await service.check_username_usable(user_sign_up.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username `{user_sign_up.username}` already exists"
        )

    user = await service.create_user(user_sign_up.username, user_sign_up.password)
    request.session["user_id"] = user.id
    resp = ResponseModel(
        message=f"Create new user: {user.username}",
        data=user
    )
    return resp


@router.post("/login", response_model=ResponseModel)
async def handle_user_log_in(user_log_in: UserRequest, request: Request):
    try:
        user = await service.get_user_by_username_and_password(user_log_in.username, user_log_in.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    request.session["user_id"] = user.id

    resp = ResponseModel(
        message=f"Welcome, {user.username}!",
        data=user
    )
    return resp


@router.post("/logout")
async def handle_user_log_out(request: Request):
    request.session.clear()
    return {"message": f"Bye."}


@router.get("/user/{username}", response_model=ResponseModel)
async def handle_get_user_by_username(username, request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

    try:
        user = await service.get_user_by_username(username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])
    resp = ResponseModel(
        message=f"Hi, {user.username}!",
        data=user
    )
    return resp


@router.get("/me", response_model=ResponseModel)
async def handle_get_user_by_username(request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

    try:
        user = await service.get_user_by_user_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])
    resp = ResponseModel(
        message=f"Welcome, {user.username}!",
        data=user
    )
    return resp
