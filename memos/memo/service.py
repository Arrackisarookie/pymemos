import uuid
from datetime import datetime

from memos.database import db
from memos.memo.models import Memo
from memos.memo.schemas import MemoResponse


async def create_memo(content: str, user_id: str) -> MemoResponse:
    now_datetime = datetime.now()
    memo_id = uuid.uuid4().hex
    m = {
        "id": memo_id,
        "content": content,
        "user_id": user_id,
        "created_at": now_datetime,
        "updated_at": now_datetime
    }

    query = Memo.insert()
    await db.execute(query=query, values=m)
    return MemoResponse(
        id=memo_id,
        content=content,
        created_at=now_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=now_datetime.strftime("%Y-%m-%d %H:%M:%S")
    )


async def update_memo(memo_id: str, content: str):
    now_datetime = datetime.now()
    m = await get_memo_by_id(memo_id)

    updated_memo = {
        "content": content,
        "updated_at": now_datetime
    }

    query = Memo.update().where(Memo.c.id == memo_id)
    await db.execute(query=query, values=updated_memo)

    return MemoResponse(
        id=memo_id,
        content=content,
        created_at=m.created_at,
        updated_at=now_datetime.strftime("%Y-%m-%d %H:%M:%S")
    )


async def delete_memo(memo_id: str):
    now_datetime = datetime.now()
    m = await get_memo_by_id(memo_id)

    updated_memo = {
        "updated_at": now_datetime,
        "deleted_at": now_datetime
    }

    query = Memo.update().where(Memo.c.id == memo_id)
    await db.execute(query=query, values=updated_memo)

    return MemoResponse(
        id=memo_id,
        content=m.content,
        created_at=m.created_at,
        updated_at=now_datetime.strftime("%Y-%m-%d %H:%M:%S")
    )


async def get_memo_by_id(memo_id: str) -> MemoResponse:
    query = Memo.select().where(Memo.c.id == memo_id)
    m = await db.fetch_one(query)

    if m is None:
        raise ValueError("No such memo")

    return MemoResponse(
        id=m.id,
        content=m.content,
        created_at=m.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=m.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    )


async def get_all_memos() -> list[MemoResponse]:
    query = Memo.select().where(Memo.c.deleted_at.is_(None))
    memos = await db.fetch_all(query)

    return [
        MemoResponse(
            id=m.id,
            content=m.content,
            created_at=m.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=m.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        )
        for m in memos
    ]


async def get_deleted_memos() -> list[MemoResponse]:
    query = Memo.select().where(Memo.c.deleted_at.isnot(None))
    memos = await db.fetch_all(query)

    return [
        MemoResponse(
            id=m.id,
            content=m.content,
            created_at=m.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=m.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        )
        for m in memos
    ]
