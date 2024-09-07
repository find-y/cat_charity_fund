from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_not_duplicated,
    check_project_is_open,
    check_project_not_fully_invested,
    validate_invested_amount_zero,
    validate_new_full_amount_less_invested,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investition import close_fully_invested, invest

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary="Создает проект. Доступно только суперюзерам.",
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_not_duplicated(charity_project.name, session)

    charity_project = await charity_project_crud.create(
        charity_project, session
    )
    return await invest(charity_project, donation_crud, session)


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    summary="Возвращает список всех проектов.",
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_all(session)


@router.delete(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary="Удаляет проект. Доступно только суперюзерам.",
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await charity_project_crud.get_or_404(
        charity_project_id, session
    )
    validate_invested_amount_zero(charity_project.invested_amount)
    check_project_is_open(charity_project.close_date)
    return await charity_project_crud.remove(charity_project, session)


@router.patch(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary="Обновляет проект. Доступно только суперюзерам.",
)
async def partially_update_charity_project_id(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await charity_project_crud.get_or_404(
        charity_project_id, session
    )
    check_project_not_fully_invested(charity_project)
    if obj_in.name is not None:
        await check_name_not_duplicated(obj_in.name, session)
    if obj_in.full_amount is not None:
        validate_new_full_amount_less_invested(
            obj_in.full_amount, charity_project.invested_amount
        )
        charity_project = await close_fully_invested(
            obj_in.full_amount, charity_project, session
        )
    return await charity_project_crud.update(charity_project, obj_in, session)
