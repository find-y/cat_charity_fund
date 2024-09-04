from fastapi import APIRouter, Depends
from fastapi import HTTPException
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
    invested_amount_zero,
    is_opened,
    no_name_duplicate,
    new_full_less_than_invested
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
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await no_name_duplicate(charity_project.name, session)

    charity_project = await charity_project_crud.create(
        charity_project, session)
    charity_project = await add_donations_to_project(charity_project, session)
    return charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
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
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров"""
    charity_project = await charity_project_crud.get_or_exception(
        charity_project_id, session)
    invested_amount_zero(charity_project.invested_amount)
    is_opened(charity_project.close_date)
    charity_project = await charity_project_crud.remove(
        charity_project, session)
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project_id(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await charity_project_crud.get_or_exception(
        charity_project_id, session)

    if charity_project.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Проект уже закрыт, менять нельзя.',
        )
    if obj_in.name is not None:
        await no_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        new_full_less_than_invested(
            obj_in.full_amount, charity_project.invested_amount)
        charity_project = await close_fully_invested(
            obj_in.full_amount, charity_project, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project
