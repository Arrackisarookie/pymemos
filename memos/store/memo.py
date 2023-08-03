import uuid
from datetime import datetime

from sqlalchemy.engine import Row

from memos.store import db, Memo


async def create_memo(content: str, user_id: str):
    now_datetime = datetime.now()
    memo = {
        "memo_id": uuid.uuid4().hex,
        "content": content,
        "user_id": user_id,
        "created_at": now_datetime,
        "updated_at": now_datetime
    }

    query = Memo.insert()
    await db.execute(query=query, values=memo)
    return memo


async def update_memo(memo_id: str, content: str):
    now_datetime = datetime.now()
    await get_memo_by_id(memo_id)

    updated_memo = {
        "content": content,
        "updated_at": now_datetime
    }

    query = Memo.update().where(Memo.c.memo_id == memo_id)
    await db.execute(query=query, values=updated_memo)


async def delete_memo(memo_id: str):
    now_datetime = datetime.now()
    await get_memo_by_id(memo_id)

    updated_memo = {
        "updated_at": now_datetime,
        "deleted_at": now_datetime
    }

    query = Memo.update().where(Memo.c.memo_id == memo_id)
    await db.execute(query=query, values=updated_memo)


async def get_memo_by_id(memo_id: str) -> Row:
    query = Memo.select().where(Memo.c.memo_id == memo_id)
    memo = await db.fetch_one(query)

    if memo is None:
        raise ValueError("No such memo")

    return memo


async def get_memos_by_user_id(user_id: str) -> list[Memo]:
    query = Memo.select().where(Memo.c.user_id == user_id)
    memos = await db.fetch_all(query)

    return memos


async def get_all_memos() -> list[Memo]:
    query = Memo.select()
    memos = await db.fetch_all(query)

    return memos
