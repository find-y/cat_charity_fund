from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, validator, Extra


class CharityProjectBase(BaseModel):
    # name: Optional[str] = Field(None, min_length=1, max_length=100)
    # description: Optional[str]

    # name = Column(String(100), unique=True, nullable=False)
    # description = Column(Text, nullable=False)
    # full_amount = Column(Integer, nullable=False)

    # invested_amount = Column(Integer, default=0, nullable=False)
    # fully_invested = Column(Boolean, default=False, nullable=False)
    # create_date = Column(DateTime, default=func.now(), nullable=False)
    # # может вынести в базовый класс?
    # close_date = Column(DateTime)

    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]

    invested_amount: Optional[int]  #= Field(None, example="10")
    fully_invested: Optional[int]  #= Field(None)
    create_date: Optional[datetime] ##
    close_date: Optional[datetime] = Field(None) # не убирает из примеров

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    # name: str = Field(..., min_length=1, max_length=100)
    name: str = Field(...)
    full_amount: int = Field(...)
    # create_date: datetime = Field(...)

# class CharityProjectUpdate(CharityProjectBase):
#     pass


class CharityProjectUpdate(CharityProjectBase):
    # @validator('name')
    # def name_cannot_be_null(cls, value):
    #     if value is None:
    #         raise ValueError('Имя переговорки не может быть пустым!')
    #     return value
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True