import logging

from fastapi import FastAPI, APIRouter

from memos.api import auth_router, memo_router
from memos.store import db


app = FastAPI(
    title="Memos",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)
log = logging.getLogger("memos")


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
