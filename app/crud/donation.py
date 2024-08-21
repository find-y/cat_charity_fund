from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDMeetingRoom(CRUDBase):
    pass

donation_crud = CRUDMeetingRoom(Donation)