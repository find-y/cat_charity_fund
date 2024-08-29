# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.crud.charity_project import charity_project_crud
# from app.crud.donation import donation_crud

from app.models import CharityProject, Donation #, User


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
        )  # в документации такое сообщение не прописано


def new_full_more_than_invested(
        new_full: int,
        invested: int,
) -> None:
    """проверяет, что проект не закрыт"""
    if new_full < invested:
        raise HTTPException(
            status_code=400,
            detail='Нелья установить значение full_amount меньше уже вложенной суммы.'
        )


# async def check_meeting_room_exists(
#         meeting_room_id: int,
#         session: AsyncSession,
# ) -> MeetingRoom:
#     meeting_room = await meeting_room_crud.get(meeting_room_id, session)
#     if meeting_room is None:
#         raise HTTPException(
#             status_code=404,
#             detail='Переговорка не найдена!'
#         )
#     return meeting_room


# async def check_reservation_intersections(**kwargs) -> None:
#     reservations = await reservation_crud.get_reservations_at_the_same_time(
#         **kwargs)
#     if reservations:
#         raise HTTPException(
#             status_code=422,
#             detail={
#                 "error": "No reservations found",
#                 "reservations": str(reservations)})


# async def object_exists(
#         id: int,
#         obj_crud,
#         session: AsyncSession,
#         # user: User,
# ) -> CharityProject:
#     """проверяет, существует ли запрошенный объект"""
#     obj = await obj_crud.get(
#         obj_id=id, session=session)
#     if not obj:
#         raise HTTPException(
#             status_code=404,
#             detail='Объект не найден!'
#         )
#     # if reservation.user_id != user.id and not user.is_superuser:
#     #     raise HTTPException(
#     #         status_code=403,
#     #         detail='Невозможно редактировать или удалить чужую бронь!'
#     #     )
#     return obj

# async def invested_amount_zero(
#         id: int,
#         obj_crud,
#         session: AsyncSession,
#         # user: User,
# ) -> CharityProject:
#     """проверяет, что не было донатов в проект"""
#     obj = await obj_crud.get(
#         obj_id=id, session=session)
#     if obj.invested_amount != 0:
#         raise HTTPException(
#             status_code=400,
#             detail='В проект были внесены средства, не подлежит удалению!'
#         )