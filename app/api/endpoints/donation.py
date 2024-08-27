from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.core.user import current_user
from app.models import User

from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationBase, DonationCreate, DonationDB, DonationUser
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
        user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    donations = await donation_crud.get_multi(session)
    return donations


# @router.get(
#     '/my',
#     response_model=list[DonationUser],
#     response_model_exclude={'user_id'},
# )
# async def get_my_donations(
#     session: AsyncSession = Depends(get_async_session),
#     user: User = Depends(current_user)
# ):
#     """Получает список всех бронирований для текущего пользователя."""
#     donations = await donation_crud.get_by_user(
#         session=session, user=user
#     )
#     return donations