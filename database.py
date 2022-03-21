from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine
)

from databases import Database

DATABASE_URL = "postgresql://admin:1@localhost/medium"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

Article = Table(
    "article",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(199)),
    Column("description", String(199)),
)

database = Database(DATABASE_URL)
