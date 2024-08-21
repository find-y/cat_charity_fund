from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy import Column, Integer
from sqlalchemy.orm import (
    declarative_base,
    declared_attr,
    sessionmaker,
)
from app.core.config import settings

#базовый класс из вебинара для sqlalchemy2
'''
from sqlalchemy.orm import (
    DeclarativeBase, #
    Mapped,
    mapped_column, #
    declared_attr,
)
class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    @declared_attr.directive()
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
'''

class PreBase:

    @declared_attr
    def __tablename__(cls):
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()
    # Во все таблицы будет добавлено поле ID.
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
