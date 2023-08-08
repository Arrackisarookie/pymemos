from fastapi import APIRouter, Request, status
from starlette.exceptions import HTTPException

from memos.memo import service
from memos.memo.schemas import MemoRequest
from memos.schemas import ResponseModel

router = APIRouter()


@router.get("/memo", response_model=ResponseModel)
async def handle_get_all_memos(request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

    memos = await service.get_all_memos()
    return ResponseModel(
        message=f"success",
        data=memos
    )


@router.post("/memo", status_code=status.HTTP_201_CREATED, response_model=ResponseModel)
async def handle_create_memo(memo: MemoRequest, request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

    m = await service.create_memo(memo.content, user_id)

    return ResponseModel(
        message=f"Create a new memo: {m.content}",
        data=m
    )


@router.patch("/memo/{memo_id}", response_model=ResponseModel)
async def handle_update_memo(memo_id, memo: MemoRequest, request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

    try:
        m = await service.update_memo(memo_id, memo.content)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])

    return ResponseModel(
        message=f"Update a memo `{memo_id}`",
        data=m
    )


@router.get("/memo/{memo_id}", response_model=ResponseModel)
async def handle_get_memo_by_id(memo_id, request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

    try:
        m = await service.get_memo_by_id(memo_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])

    return ResponseModel(
        message="success",
        data=m
    )


@router.delete("/memo/{memo_id}", response_model=ResponseModel)
async def handle_delete_memo(memo_id, request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

    try:
        m = await service.delete_memo(memo_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])

    return ResponseModel(
        message=f"Deleted memo `{memo_id}`",
        data=m
    )


@router.get("/trash/memo", response_model=ResponseModel)
async def handle_get_deleted_memo(request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

    try:
        deleted_memos = await service.get_deleted_memos()
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])

    return ResponseModel(
        message="success",
        data=deleted_memos
    )
