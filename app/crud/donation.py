from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBaseInvest
from app.models import Donation, User


class CRUDDonation(CRUDBaseInvest):
    async def get_by_user(
        self, session: AsyncSession, user: User
    ) -> List[Donation]:
        """Получить донаты пользователя."""
        return await self.filter(session, user_id=user.id)


donation_crud = CRUDDonation(Donation)
