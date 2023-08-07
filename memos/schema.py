from typing import Any

from pydantic import BaseModel


class ResponseModel(BaseModel):
    succeed: bool = True
    status: int = 200
    message: str = ""
    data: Any


class BaseResponse(BaseModel):
    id: str
    created_at: str
    updated_at: str
