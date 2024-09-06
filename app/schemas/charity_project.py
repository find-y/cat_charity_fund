from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from pydantic import (
    BaseModel,
    Extra,
    Field,
    NonNegativeInt,
    PositiveInt,
    validator,
)


class CharityProjectBase(BaseModel):
    """
    Базовая модель для проекта.
    """

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """
    Модель для создания проекта.
    """

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt = Field(...)

    @validator("description")
    def description_not_empty(cls, value):
        """
        Проверяет, что описание не пустое.
        """
        if value.strip() == "":
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="Описание не может быть пустым.",
            )
        return value


class CharityProjectResponse(CharityProjectCreate):
    """
    Модель ответа с данными проекта.
    """

    invested_amount: Optional[NonNegativeInt]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    """
    Модель для обновления проекта.
    """


class CharityProjectDB(CharityProjectResponse):
    """
    Модель базы данных проекта.
    """

    id: int

    class Config:
        orm_mode = True
