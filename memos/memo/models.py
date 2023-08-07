from datetime import datetime

from sqlalchemy import Table, Column, String, TEXT, ForeignKey, TIMESTAMP

from memos.database import metadata

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
Comment = Table(
    "comments",
    metadata,
    Column("id", String, primary_key=True),
    Column("content", TEXT),
    Column("memo_id", None, ForeignKey("memos.id")),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Column("updated_at", TIMESTAMP, default=datetime.now),
    Column("deleted_at", TIMESTAMP, default=datetime.now)
)
