from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import CharityDonationBase


class Donation(CharityDonationBase):
    """Модель доната."""

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    comment = Column(Text)

    def __str__(self) -> str:
        return self.full_amount
