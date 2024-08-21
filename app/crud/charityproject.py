from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charityproject import CharityProject


class CRUDMeetingRoom(CRUDBase):
    pass

charity_project_crud = CRUDMeetingRoom(CharityProject)