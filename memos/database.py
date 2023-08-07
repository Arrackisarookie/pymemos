from databases import Database
from sqlalchemy import MetaData

from memos.config import get_settings

settings = get_settings()
db = Database(settings.DATABASE_URL)
metadata = MetaData()
