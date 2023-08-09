from datetime import datetime
from typing import Any

import orjson
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, root_validator


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=None)

    return dt.strftime("%Y-%m-%d %H:%M:%S%z")


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {datetime: convert_datetime_to_gmt}  # method for custom JSON encoding of datetime fields

    @classmethod
    @root_validator()
    def set_null_microseconds(cls, data: dict) -> dict:
        """Drops microseconds in all the datetime field values."""
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = super().dict(**kwargs)

        return jsonable_encoder(default_dict)


class ResponseModel(ORJSONModel):
    succeed: bool = True
    status: int = 200
    message: str = ""
    data: Any


class BaseResponse(ORJSONModel):
    id: str
    created_at: datetime
    updated_at: datetime
