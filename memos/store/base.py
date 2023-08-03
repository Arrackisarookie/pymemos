from datetime import datetime

from databases import Database
from sqlalchemy import MetaData, Table, Column, String, TIMESTAMP, TEXT, ForeignKey
from sqlalchemy.dialects import sqlite
from sqlalchemy.schema import CreateTable, DropTable

DATABASE_URL = "sqlite+aiosqlite:///resources/memos.db"

db = Database(DATABASE_URL)
metadata = MetaData()


User = Table(
    "users",
    metadata,
    Column("user_id", String, primary_key=True),
    Column("username", String, unique=True),
    Column("password", String),
    Column("wx_openid", String),
    Column("github_name", String),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Column("updated_at", TIMESTAMP, default=datetime.now)
)

Memo = Table(
    "memos",
    metadata,
    Column("memo_id", String, primary_key=True),
    Column("content", TEXT),
    Column("user_id", None, ForeignKey("users.user_id")),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Column("updated_at", TIMESTAMP, default=datetime.now),
    Column("deleted_at", TIMESTAMP, default=datetime.now)
)


async def init_tables():
    for table in metadata.tables.values():
        schema = DropTable(table, if_exists=True)
        query = str(schema.compile(dialect=sqlite.dialect()))
        await db.execute(query=query)

        schema = CreateTable(table, if_not_exists=True)
        query = str(schema.compile(dialect=sqlite.dialect()))
        await db.execute(query=query)
