from typing import Optional
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charityproject import CharityProject


class CRUDCharityProject(CRUDBase):
        # Преобразуем функцию в метод класса.
    async def get_proj_id_by_name(
            # Дописываем параметр self.
            # В качестве альтернативы здесь можно
            # применить декоратор @staticmethod.
            self,
            proj_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_room_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == proj_name
            )
        )
        db_room_id = db_room_id.scalars().first()
        return db_room_id

    async def get_or_exception(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> CharityProject:
        obj = await self.get(
            obj_id=obj_id, session=session)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail='Объект не найден!'
            )
        return obj


charity_project_crud = CRUDCharityProject(CharityProject)