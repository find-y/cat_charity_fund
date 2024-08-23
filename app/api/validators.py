# app/api/validators.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# from app.crud.charityproject import charity_project_crud
# from app.crud.donation import donation_crud

from app.models import CharityProject, Donation #, User



# async def check_name_duplicate(
#         room_name: str,
#         session: AsyncSession,
# ) -> None:
#     room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
#     if room_id is not None:
#         raise HTTPException(
#             status_code=422,
#             detail='Переговорка с таким именем уже существует!',
#         )


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


async def object_exists(
        id: int,
        obj_crud,
        session: AsyncSession,
        # user: User,
) -> CharityProject:
    """проверяет, существует ли запрошенный объект"""
    obj = await obj_crud.get(
        obj_id=id, session=session)
    if not obj:
        raise HTTPException(
            status_code=404,
            detail='Объект не найден!'
        )
    # if reservation.user_id != user.id and not user.is_superuser:
    #     raise HTTPException(
    #         status_code=403,
    #         detail='Невозможно редактировать или удалить чужую бронь!'
    #     )
    return obj
