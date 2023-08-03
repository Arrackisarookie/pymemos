import re
from typing import Optional

from fastapi import APIRouter, Cookie, Response, status
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from memos import store

router = APIRouter()


class Memo(BaseModel):
    content: str


@router.get("/memo")
async def handle_get_all_memos():
    return await store.get_all_memos()


@router.post("/memo", status_code=status.HTTP_201_CREATED)
async def handle_create_memo(memo: Memo, user_id: Optional[str] = Cookie(default=None)):
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")
    m = await store.create_memo(memo.content, user_id)

    return {"message": f"Create a new memo: {m['memo_id']}"}


@router.patch("/memo/{memo_id}")
async def handle_update_memo(memo_id, memo: Memo):
    try:
        await store.update_memo(memo_id, memo.content)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])
