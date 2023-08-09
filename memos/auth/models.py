from datetime import datetime

from sqlalchemy import Table, Column, String, TIMESTAMP

from memos.database import metadata

User = Table(
    "user",
    metadata,
    Column("id", String, primary_key=True),
    Column("username", String, unique=True),
    Column("password", String),
    Column("wx_openid", String),
    Column("github_name", String),
    Column("created_at", TIMESTAMP, default=datetime.now),
    Column("updated_at", TIMESTAMP, default=datetime.now)
)
