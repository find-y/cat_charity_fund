from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationUser
from app.services.investition import invest

router = APIRouter()


@router.post("/", response_model=DonationUser, summary="Создает донат.")
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    return await invest(new_donation, charity_project_crud, session)


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
    return await donation_crud.get_all(session)


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
    return await donation_crud.get_by_user(session=session, user=user)
