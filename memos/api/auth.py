import re
from typing import Optional

from fastapi import APIRouter, status, Response, Cookie
from pydantic import Field, field_validator, BaseModel
from starlette.exceptions import HTTPException

from memos import store

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*.,_])[A-Za-z\d!@#$%^&*.,_]{6,128}$")

router = APIRouter()


class UserSignUp(BaseModel):
    username: str
    password: str = Field(min_length=6, max_length=128)

    @field_validator("password")
    def valid_password(cls, p: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, p):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "one digit and one special symbol"
            )
        return p


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def handle_user_sign_up(user: UserSignUp):
    if not await store.check_username_usable(user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Username `{user.username}` already exists")
    await store.create_user(user.username, user.password)
    return {"message": f"Create new user: {user.username}"}


class UserLogIn(BaseModel):
    username: str
    password: str


@router.post("/login")
async def handle_user_log_in(user: UserLogIn, response: Response):
    try:
        user_log_in = await store.get_user_by_username_and_password(user.username, user.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    response.set_cookie(key="user_id", value=user_log_in["user_id"], expires=3600*24*30)
    return {"message": f"Welcome, {user.username}!"}


@router.post("/logout")
async def handle_user_log_out(response: Response):
    response.set_cookie(key="user_id", value="", expires=0)
    return {"message": f"Bye."}


@router.get("/user/{username}")
async def handle_get_user_by_username(username):
    try:
        user = await store.get_user_by_username(username)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])
    return user


@router.get("/me")
async def handle_get_user_by_username(user_id: Optional[str] = Cookie(default=None)):
    try:
        user = await store.get_user_by_user_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])
    return user
