from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from app.crud.base import CRUDBaseInvest
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBaseInvest):
    pass


charity_project_crud = CRUDCharityProject(CharityProject)
