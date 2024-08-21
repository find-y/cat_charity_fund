from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
# from app.core.user import current_superuser

from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charityproject import (
    CharityProjectBase, CharityProjectCreate, CharityProjectDB,
)
# from app.schemas.donation import ReservationDB
# from app.api.validators import check_name_duplicate, check_meeting_room_exists

router = APIRouter()

@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    # dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    # """Только для суперюзеров."""
    # # Выносим проверку дубликата имени в отдельную корутину.
    # # Если такое имя уже существует, то будет вызвана ошибка HTTPException
    # # и обработка запроса остановится.
    # await check_name_duplicate(meeting_room.name, session)
    charity_project = await charity_project_crud.create(charity_project, session)
    return charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
    # user: User = Depends(current_user),
):
    # """Для суперюзеров или создателей объекта бронирования"""
    # charity_project = await check_charity_project_before_edit(
    #     charity_project_id, session, user)
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session)
    charity_project = await charity_project_crud.remove(
        charity_project, session)
    return charity_project