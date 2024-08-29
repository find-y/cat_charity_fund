from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser

from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charityproject import (
    CharityProjectBase,
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
    CharityProjectResponse
)
# from app.schemas.donation import ReservationDB
from app.api.validators import (
                                # object_exists,
                                invested_amount_zero,
                                is_opened,
                                check_name_duplicate
                                )  #check_name_duplicate, check_meeting_room_exists

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    # response_model_exclude_none=True,
    # response_model_exclude_unset=True,  # не убирает из примеров
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    charity_project = await charity_project_crud.create(charity_project, session)
    return charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    # response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.delete(  #добавить проверку, что нет денег
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
    invested_amount_zero(charity_project)
    is_opened(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project, session)
    return charity_project


@router.patch(
    '/{meeting_room_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(  #добавить проверку, что сумма не меньше внесенной
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    # charity_project = await object_exists(
    #     charity_project_id, charity_project_crud, session)
    charity_project = await charity_project_crud.get_or_exception(
        charity_project_id, session)

    # if obj_in.name is not None:
    #     await check_name_duplicate(obj_in.name, session)

    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project