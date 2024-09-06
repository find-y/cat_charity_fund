from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import CommonBase


class Donation(CommonBase):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    comment = Column(Text)
