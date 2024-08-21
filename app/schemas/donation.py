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
    # create_date: Optional[datetime]
    close_date: Optional[datetime]


class DonationCreate(DonationBase):
    # name: str = Field(..., min_length=1, max_length=100)
    full_amount: int = Field(...)
    # create_date: int = Field(...)


# class CharityProjectUpdate(CharityProjectBase):
#     pass


class DonationDB(DonationBase):
    id: int

    class Config:
        orm_mode = True
