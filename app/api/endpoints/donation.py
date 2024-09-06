from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationUser
from app.services.investition import distribute_donation

router = APIRouter()


@router.post("/", response_model=DonationUser, summary="Создает донат.")
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    new_donation = await distribute_donation(new_donation, session)
    return new_donation


@router.get(
    "/",
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary="Возвращает список всех донатов. Доступно только суперюзерам.",
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    "/my",
    response_model=list[DonationUser],
    response_model_exclude={"user_id"},
    summary="Возвращает все донаты юзера.",
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donations = await donation_crud.get_by_user(session=session, user=user)
    return donations
