from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    async def get_by_user(self, session: AsyncSession, user: User):
        reservations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return reservations.scalars().all()

    async def get_open_donations_sorted(self, session: AsyncSession):
        """получить список донейшнов,
        отсортированных по дате создания от старого к новому,
        в которых fully_invested = False"""
        stmt = (
            select(donation_crud.model)
            .filter(donation_crud.model.fully_invested == 0)
            .order_by(donation_crud.model.create_date)
        )
        donations = await session.execute(stmt)
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
