from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


async def check_name_not_duplicated(
    obj_name: str,
    session: AsyncSession,
) -> None:
    """проверяет, что имя не занято"""
    obj_id = await charity_project_crud.get_proj_id_by_name(obj_name, session)
    if obj_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Проект с таким именем уже существует!",
        )


def validate_invested_amount_zero(
    invested_amount: int,
) -> None:
    """проверяет, что не было донатов в проект"""
    if invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


def check_project_is_open(
    close_date: datetime,
) -> None:
    """проверяет, что проект открыт"""
    if close_date:
        raise HTTPException(
            status_code=400, detail="Проект закрыт, не подлежит удалению!"
        )


def validate_new_full_amount_less_invested(
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
            detail=(
                "Нельзя установить значение full_amount "
                "меньше уже вложенной суммы."
            ),
        )


def check_project_not_fully_invested(charity_project) -> None:
    """
    Проверяет, что проект еще не полностью инвестирован,
    и не закрыт соответственно.
    """
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400, detail="Проект уже закрыт, менять нельзя."
        )
