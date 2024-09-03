from typing import Optional
from datetime import datetime
from fastapi import HTTPException

from pydantic import (
    BaseModel, Field, validator, Extra, PositiveInt, NonNegativeInt)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt = Field(...)

    @validator('description')
    def description_not_empty(cls, value):
        if value.strip() == "":
            raise HTTPException(status_code=422,
                                detail="Описание не может быть пустым.")
        return value


class CharityProjectResponse(CharityProjectCreate):
    invested_amount: Optional[NonNegativeInt]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectResponse):
    id: int

    class Config:
        orm_mode = True