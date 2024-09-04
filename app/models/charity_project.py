from sqlalchemy import Column, String, Text

from .base import CommonBase


class CharityProject(CommonBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
