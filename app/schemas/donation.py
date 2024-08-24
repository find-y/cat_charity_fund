from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator


class DonationBase(BaseModel):
    # user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # comment = Column(Text)
    # full_amount = Column(Integer, nullable=False)
    # invested_amount = Column(Integer, default=0, nullable=False)
    # fully_invested = Column(Boolean, default=False, nullable=False)
    # create_date = Column(DateTime, default=func.now(), nullable=False)
    # close_date = Column(DateTime)
    comment: Optional[str]
    full_amount: Optional[int]
    invested_amount: Optional[int]
    fully_invested: Optional[int]
    close_date: Optional[datetime]


class DonationCreate(DonationBase):
    full_amount: int = Field(...)


class DonationDB(DonationBase):
    id: int
    # user_id: Optional[int]

    class Config:
        orm_mode = True


# class DonationUser(DonationBase):
#     id: int
#     comment: Optional[str]
#     full_amount: int
#     create_date: datetime

#     class Config:
#         orm_mode = True
