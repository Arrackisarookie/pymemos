import re
from typing import Optional, Any

from pydantic import BaseModel, Field, field_validator

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*.,_])[A-Za-z\d!@#$%^&*.,_]{6,128}$")


class ResponseModel(BaseModel):
    succeed: bool = True
    status: int = 200
    message: str = ""
    data: Any


class UserRequest(BaseModel):
    username: str
    password: str = Field(min_length=6, max_length=128)

    @field_validator("password")
    def valid_password(cls, p: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, p):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "one digit and one special symbol"
            )
        return p


class MemoRequest(BaseModel):
    content: str


class BaseResponse(BaseModel):
    id: str
    created_at: str
    updated_at: str


class UserResponse(BaseResponse):
    username: str
    github_name: Optional[str]
    wx_openid: Optional[str]


class MemoResponse(BaseResponse):
    content: str
