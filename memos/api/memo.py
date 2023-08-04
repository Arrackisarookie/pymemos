from typing import Optional

from fastapi import APIRouter, Cookie, status
from starlette.exceptions import HTTPException

from memos import store
from memos.schema import MemoResponse, ResponseModel, MemoRequest

router = APIRouter()


@router.get("/memo", response_model=ResponseModel)
async def handle_get_all_memos():
    memos = await store.get_all_memos()
    return ResponseModel(
        message=f"success",
        data=memos
    )


@router.post("/memo", status_code=status.HTTP_201_CREATED, response_model=ResponseModel)
async def handle_create_memo(memo: MemoRequest, user_id: Optional[str] = Cookie(default=None)):
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")
    m = await store.create_memo(memo.content, user_id)

    return ResponseModel(
        message=f"Create a new memo: {m.content}",
        data=m
    )


@router.patch("/memo/{memo_id}")
async def handle_update_memo(memo_id, memo: MemoRequest):
    try:
        m = await store.update_memo(memo_id, memo.content)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])

    return ResponseModel(
        message=f"Update a memo `{memo_id}`",
        data=m
    )
