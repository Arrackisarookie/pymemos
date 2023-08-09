from datetime import datetime

from sqlalchemy import Table, Column, String, TEXT, ForeignKey, TIMESTAMP

from memos.database import metadata

Memo = Table(
    "memo",
    metadata,
    Column("id", String, primary_key=True),
    Column("content", TEXT),
    Column("user_id", None, ForeignKey("user.id")),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Column("updated_at", TIMESTAMP, default=datetime.now),
    Column("deleted_at", TIMESTAMP, default=datetime.now)
)
Comment = Table(
    "comment",
    metadata,
    Column("id", String, primary_key=True),
    Column("content", TEXT),
    Column("memo_id", None, ForeignKey("memo.id")),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Column("updated_at", TIMESTAMP, default=datetime.now),
    Column("deleted_at", TIMESTAMP, default=datetime.now)
)
