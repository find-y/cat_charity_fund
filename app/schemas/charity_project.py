from typing import Optional
from datetime import datetime, timezone
from fastapi import HTTPException

from pydantic import BaseModel, Field, validator, Extra, PositiveInt, NonNegativeInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(...)
    # description: str = Field(..., min_length=1)
    full_amount: PositiveInt = Field(...)

    @validator('description')
    def description_not_empty(cls, v):
        if v.strip() == "":
            raise HTTPException(status_code=422, detail="Description cannot be empty.")
        return v


class CharityProjectResponse(CharityProjectCreate):
    invested_amount: Optional[NonNegativeInt]  #= Field(None, example="10")
    fully_invested: Optional[bool]  #= Field(None)
    create_date: Optional[datetime] ##
    close_date: Optional[datetime] #= Field(None) # не убирает из примеров

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    # @validator('name')
    # def name_cannot_be_null(cls, value):
    #     if value is None:
    #         raise ValueError('Имя переговорки не может быть пустым!')
    #     return value

    pass


class CharityProjectDB(CharityProjectResponse):
    id: int

    class Config:
        orm_mode = True