from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.api.validators import (
    validate_invested_amount_zero,
    check_project_is_open,
    check_name_not_duplicated,
    validate_new_full_amount_less_invested,
    check_project_not_fully_invested
)
from app.services.investition import (
    add_donations_to_project,
    close_fully_invested
)


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Создает проект. Доступно только суперюзерам.'
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_name_not_duplicated(charity_project.name, session)

    charity_project = await charity_project_crud.create(
        charity_project, session)
    charity_project = await add_donations_to_project(charity_project, session)
    return charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    summary='Возвращает список всех проектов.'
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Удаляет проект. Доступно только суперюзерам.'
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await charity_project_crud.get_or_exception(
        charity_project_id, session)
    validate_invested_amount_zero(charity_project.invested_amount)
    check_project_is_open(charity_project.close_date)
    charity_project = await charity_project_crud.remove(
        charity_project, session)
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Обновляет проект. Доступно только суперюзерам.'
)
async def partially_update_charity_project_id(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await charity_project_crud.get_or_exception(
        charity_project_id, session)
    check_project_not_fully_invested(charity_project)
    if obj_in.name is not None:
        await check_name_not_duplicated(obj_in.name, session)
    if obj_in.full_amount is not None:
        validate_new_full_amount_less_invested(
            obj_in.full_amount, charity_project.invested_amount)
        charity_project = await close_fully_invested(
            obj_in.full_amount, charity_project, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
