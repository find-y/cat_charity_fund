from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


async def check_name_not_duplicated(
    obj_name: str,
    session: AsyncSession,
) -> None:
    """Проверяет, что имя не занято."""
    existing_obj = await charity_project_crud.filter(session, name=obj_name)
    if existing_obj:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )


def validate_invested_amount_zero(
    invested_amount: int,
) -> None:
    """Инвестированная сумма равна нулю."""
    if invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="В проект были внесены средства, не подлежит удалению!",
        )


def check_project_is_open(
    close_date: datetime,
) -> None:
    """Проверяет, что проект открыт."""
    if close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект закрыт, не подлежит удалению!",
        )


def validate_new_full_amount_less_invested(
    new_full: int,
    invested: int,
) -> None:
    """
    Проверяет, что новая сумма не меньше cделанных вложений.
    """
    if new_full < invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Нельзя установить значение full_amount "
                "меньше уже вложенной суммы."
            ),
        )


def check_project_not_fully_invested(charity_project) -> None:
    """
    Проект не является полностью проинвестированным.
    """
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект уже закрыт, менять нельзя.",
        )
