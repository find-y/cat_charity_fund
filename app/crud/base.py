from typing import Any, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User

T = TypeVar('T')


class CRUDBase:

    def __init__(self, model: Type[T]):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[T]:
        """Получить объект по ID."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_by_kwargs(
        self,
        session: AsyncSession,
        **kwargs: Any
    ) -> Optional[list]:
        """Получить объекты по ключевым словам."""
        query = select(self.model).filter_by(**kwargs)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_multi(self, session: AsyncSession):
        """Получить все объекты модели."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None
    ) -> T:
        """Создать новый объект."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["user_id"] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ) -> T:
        """Обновить существующий объект."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ) -> T:
        """Удалить объект."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_open_obj_sorted(
        self,
        session: AsyncSession
    ) -> List[T]:
        """Получить отсортированные открытые объекты.

        Отсортированные по дате создания от старого к новому,
        в которых fully_invested = False"""
        stmt = (
            select(self.model)
            .where(self.model.fully_invested == 0)
            .order_by(self.model.create_date)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
