import logging
from typing import Dict

from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse

from memos.api import auth_router, memo_router
from memos.store import db, init_tables


app = FastAPI(
    title="Memos",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)
log = logging.getLogger("memos")


@app.get('/healthcheck', include_in_schema=False)
async def healthcheck() -> Dict[str, str]:
    return {'status': 'ok'}


@app.get('/init', include_in_schema=False)
async def init() -> Dict[str, str]:
    await init_tables()
    return {'status': 'ok'}


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
