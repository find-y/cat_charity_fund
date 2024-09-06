from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBaseInvest
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBaseInvest):
    async def get_proj_id_by_name(
        self,
        proj_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """Получить ID проекта по названию."""
        project = await self.get_by_kwargs(session, name=proj_name)
        return project[0].id if project else None

    async def get_or_exception(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> CharityProject:
        """Получить объект или вызвать исключение."""
        obj = await self.get(obj_id=obj_id, session=session)
        if not obj:
            raise HTTPException(status_code=404, detail="Объект не найден!")
        return obj


charity_project_crud = CRUDCharityProject(CharityProject)
