from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class CommonBase(Base):
    """Абстрактная база данных с общими полями для проектов и донатов."""

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime)

    # def left(self) -> int:
    #     """Возвращает оставшуюся сумму инвестиций в проекте."""
    #     return self.full_amount - self.invested_amount

    # def close(self) -> None:
    #     """Закрывает проект как полностью инвестированный."""
    #     self.invested_amount = self.full_amount
    #     self.fully_invested = True
    #     self.close_date = datetime.now()
