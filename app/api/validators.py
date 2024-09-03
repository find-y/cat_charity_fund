from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


async def check_name_duplicate(
        obj_name: str,
        session: AsyncSession,
) -> None:
    obj_id = await charity_project_crud.get_proj_id_by_name(obj_name, session)
    if obj_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


def invested_amount_zero(
        invested_amount: int,
) -> None:
    """проверяет, что не было донатов в проект"""
    if invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def is_opened(
        close_date: datetime,
) -> None:
    """проверяет, что проект открыт"""
    if close_date:
        raise HTTPException(
            status_code=400,
            detail='Проект закрыт, не подлежит удалению!'
        )


def new_full_more_than_invested(
        new_full: int,
        invested: int,
) -> None:
    """
    Проверяет, что новая сумма проекта
    не меньше вложенных инвестиций.
    """
    if new_full < invested:
        raise HTTPException(
            status_code=400,
            detail='''Нелья установить значение
            full_amount меньше уже вложенной суммы.'''
        )
