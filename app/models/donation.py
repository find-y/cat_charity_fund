from sqlalchemy import Column, Integer, Text, ForeignKey

from .base import CommonBase


class Donation(CommonBase):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
