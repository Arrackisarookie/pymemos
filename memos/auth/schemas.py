import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from memos.schema import BaseResponse

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*.,_])[A-Za-z\d!@#$%^&*.,_]{6,128}$")


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


class UserResponse(BaseResponse):
    username: str
    github_name: Optional[str]
    wx_openid: Optional[str]
