from pydantic import BaseModel

from memos.schema import BaseResponse


class MemoRequest(BaseModel):
    content: str


class MemoResponse(BaseResponse):
    content: str
