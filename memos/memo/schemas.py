from pydantic import BaseModel

from memos.schemas import BaseResponse


class MemoRequest(BaseModel):
    content: str


class MemoResponse(BaseResponse):
    content: str
