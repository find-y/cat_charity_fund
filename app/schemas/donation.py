from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator, Extra, NonNegativeInt


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: Optional[int]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: NonNegativeInt = Field(...)


class DonationResponse(DonationCreate):
    invested_amount: Optional[NonNegativeInt]  #= Field(None, example="10")
    fully_invested: Optional[bool]  #= Field(None) поменять на bool?
    create_date: Optional[datetime]  ##
    close_date: Optional[datetime] #= Field(None) # не убирает из примеров

    class Config:
        orm_mode = True


class DonationDB(DonationResponse):
    id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True


class DonationUser(DonationBase):
    id: int
    comment: Optional[str]
    full_amount: NonNegativeInt
    create_date: datetime

    class Config:
        orm_mode = True
