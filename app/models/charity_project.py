from sqlalchemy import Column, String, Text

from .base import CharityDonationBase


class CharityProject(CharityDonationBase):
    """Модель благотвориельного проекта."""

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __str__(self) -> str:
        return self.name[:15]
