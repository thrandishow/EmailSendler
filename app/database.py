from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


DATABASE_URL = ""
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_generator = sessionmaker(engine, AsyncSession, expire_on_commit=False)


def init_db():
    Base.metadata.create_all(engine)
