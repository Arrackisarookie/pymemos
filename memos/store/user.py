import uuid
from datetime import datetime

from memos.store import db, User


async def create_user(
    username: str,
    password: str,
    github_name: str = None,
    wx_openid: str = None
):
    now_datetime = datetime.now()
    query = User.insert()
    values = {
        "user_id": uuid.uuid4().hex,
        "username": username,
        "password": password,
        "github_name": github_name,
        "wx_openid": wx_openid,
        "created_at": now_datetime,
        "updated_at": now_datetime
    }

    await db.execute(query=query, values=values)


async def update_user(user_id: str, username: str, password: str, github_name: str, wx_openid: str):
    now_datetime = datetime.now()
    await get_user_by_user_id(user_id)

    updated_user = {}

    if username != "":
        updated_user["username"] = username
    if password != "":
        updated_user["password"] = password
    if github_name != "":
        updated_user["github_name"] = github_name
    if wx_openid != "":
        updated_user["wx_openid"] = wx_openid

    updated_user["updated_at"] = now_datetime

    query = User.update().where(User.c.user_id == user_id)
    await db.execute(query=query, values=updated_user)


async def get_user_by_user_id(user_id: str) -> dict:
    query = User.select().where(User.c.user_id == user_id)
    row = await db.fetch_one(query)

    if row is None:
        raise ValueError("No such user")

    return row


async def get_user_by_username(username: str) -> dict:
    query = User.select().where(User.c.username == username)
    row = await db.fetch_one(query)

    if row is None:
        raise ValueError("No such user")

    return row


async def get_user_by_username_and_password(username: str, password: str) -> User:
    user = await get_user_by_username(username)
    if password != user["password"]:
        raise ValueError("Wrong password")
    return user


async def check_username_usable(username: str) -> bool:
    query = User.select().where(User.c.username == username)
    row = await db.fetch_one(query)
    if row is None:
        return True
    return False
