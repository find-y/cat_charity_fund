from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt


class DonationBase(BaseModel):
    """Базовая модель для донатов."""
    comment: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    """Модель для создания доната."""
    full_amount: PositiveInt = Field(...)


class DonationResponse(DonationCreate):
    """Модель ответа с данными о донате."""
    invested_amount: Optional[NonNegativeInt]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDB(DonationResponse):
    """Модель базы данных доната."""
    id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True


class DonationUser(DonationBase):
    """Модель доната для отображения пользователю."""
    id: int
    comment: Optional[str]
    full_amount: NonNegativeInt
    create_date: datetime

    class Config:
        orm_mode = True
