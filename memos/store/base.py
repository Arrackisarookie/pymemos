from datetime import datetime

from databases import Database
from sqlalchemy import MetaData, Table, Column, String, TIMESTAMP, TEXT, ForeignKey

DATABASE_URL = "sqlite+aiosqlite:///resources/memos.db"

db = Database(DATABASE_URL)
metadata = MetaData()


User = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
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
    Column("id", String, primary_key=True),
    Column("content", TEXT),
    Column("user_id", None, ForeignKey("users.id")),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Column("updated_at", TIMESTAMP, default=datetime.now),
    Column("deleted_at", TIMESTAMP, default=datetime.now)
)
