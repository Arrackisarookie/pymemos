import logging

from fastapi import FastAPI, APIRouter
from starlette.middleware.sessions import SessionMiddleware

from memos.auth.router import router as auth_router
from memos.config import get_settings
from memos.database import db
from memos.memo.router import router as memo_router

log = logging.getLogger("memos")
settings = get_settings()

app = FastAPI(
    title="Memos",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=None
)


@app.on_event("startup")
async def startup() -> None:
    await db.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await db.disconnect()


root_router = APIRouter(prefix="/api")
root_router.include_router(auth_router, tags=["auth"])
root_router.include_router(memo_router, tags=["memo"])

app.include_router(root_router)
