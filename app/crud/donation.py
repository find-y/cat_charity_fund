from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    async def get_by_user(self, session: AsyncSession, user: User):
        return await self.get_by_kwargs(session, user_id=user.id)


donation_crud = CRUDDonation(Donation)
