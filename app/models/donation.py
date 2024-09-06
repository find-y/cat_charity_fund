from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import CommonBase


class Donation(CommonBase):
    """Модель доната."""

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    comment = Column(Text)

    def __str__(self) -> str:
        return self.full_amount
