from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator, Extra, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: Optional[int]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt = Field(...)


class DonationResponse(DonationCreate):
    invested_amount: Optional[PositiveInt]  #= Field(None, example="10")
    fully_invested: Optional[PositiveInt]  #= Field(None)
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
    full_amount: PositiveInt
    create_date: datetime

    class Config:
        orm_mode = True
