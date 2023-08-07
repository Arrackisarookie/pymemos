import uuid
from datetime import datetime

from memos.auth.models import User
from memos.auth.schemas import UserResponse
from memos.database import db


async def create_user(username: str, password: str, github_name: str = None, wx_openid: str = None) -> UserResponse:
    now_datetime = datetime.now()
    query = User.insert()
    user = {
        "id": uuid.uuid4().hex,
        "username": username,
        "password": password,
        "github_name": github_name,
        "wx_openid": wx_openid,
        "created_at": now_datetime,
        "updated_at": now_datetime
    }

    await db.execute(query=query, values=user)
    del user["password"]
    return UserResponse(**user)


async def get_user_by_user_id(user_id: str) -> UserResponse:
    query = User.select().where(User.c.id == user_id)
    row = await db.fetch_one(query)

    if row is None:
        raise ValueError("No such user")

    user = UserResponse(
        id=row.id,
        username=row.username,
        github_name=row.github_name,
        wx_openid=row.wx_openid,
        created_at=row.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=row.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    )
    return user


async def get_user_by_username(username: str) -> UserResponse:
    query = User.select().where(User.c.username == username)
    row = await db.fetch_one(query)

    if row is None:
        raise ValueError("No such user")

    user = UserResponse(
        id=row.id,
        username=row.username,
        github_name=row.github_name,
        wx_openid=row.wx_openid,
        created_at=row.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=row.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    )
    return user


async def get_user_by_username_and_password(username: str, password: str) -> UserResponse:
    query = User.select().where(User.c.username == username)
    row = await db.fetch_one(query)

    if row is None:
        raise ValueError("No such user")
    if password != row.password:
        raise ValueError("Wrong password")

    user = UserResponse(
        id=row.id,
        username=row.username,
        github_name=row.github_name,
        wx_openid=row.wx_openid,
        created_at=row.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=row.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    )

    return user


async def check_username_usable(username: str) -> bool:
    query = User.select().where(User.c.username == username)
    row = await db.fetch_one(query)
    if row is None:
        return True
    return False
