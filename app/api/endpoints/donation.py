from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
# from app.core.user import current_superuser

# from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationBase, DonationCreate, DonationDB,
)

router = APIRouter()

@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
):
    new_donation = await donation_crud.create(donation, session)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)
    return donations


# @router.delete(
#     '/{donation_id}',
#     response_model=DonationDB
# )
# async def delete_donation(
#     donation_id: int,
#     session: AsyncSession = Depends(get_async_session),
#     # user: User = Depends(current_user),
# ):
#     # """Для суперюзеров или создателей объекта бронирования"""
#     reservation = await check_reservation_before_edit(
#         reservation_id, session, user)
#     reservation = await donation_crud.remove(
#         reservation, session)
#     return reservation


# @router.patch('/{donation_id}', response_model=DonationDB)
# async def update_reservation(
#         reservation_id: int,
#         obj_in: DonationUpdate,
#         session: AsyncSession = Depends(get_async_session),
#         user: User = Depends(current_user),
# ):
#     """Для суперюзеров или создателей объекта бронирования"""
#     # Проверяем, что такой объект бронирования вообще существует.
#     reservation = await check_reservation_before_edit(
#         reservation_id, session, user
#     )
#     # Проверяем, что нет пересечений с другими бронированиями.
#     await check_reservation_intersections(
#         # Новое время бронирования, распакованное на ключевые аргументы.
#         **obj_in.dict(),
#         # id обновляемого объекта бронирования,
#         reservation_id=reservation_id,
#         # id переговорки.
#         meetingroom_id=reservation.meetingroom_id,
#         session=session
#     )
#     reservation = await reservation_crud.update(
#         db_obj=reservation,
#         # На обновление передаем объект класса ReservationUpdate, как и требуется.
#         obj_in=obj_in,
#         session=session,
#     )
#     return reservation 