from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, Extra, NonNegativeInt, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt = Field(...)


class DonationResponse(DonationCreate):
    invested_amount: Optional[NonNegativeInt]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

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
