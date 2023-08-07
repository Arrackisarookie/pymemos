from functools import lru_cache

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
