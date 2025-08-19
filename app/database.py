from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .database import DATABASE_URL


class Base(DeclarativeBase):
    pass


db_url = DATABASE_URL
engine = create_async_engine(db_url, echo=True)
async_session_generator = sessionmaker(engine, AsyncSession, expire_on_commit=False)


def init_db():
    Base.metadata.create_all(engine)
