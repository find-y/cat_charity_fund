from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
# from sqlalchemy.orm import relationship
from app.core.db import Base


class Donation(Base):   
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # charity_project_id = Column(
    #     Integer, ForeignKey('charityproject.id'), nullable=False)
    comment = Column(Text)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=func.now(), nullable=False)
    close_date = Column(DateTime)

    # user = relationship("User")

# Описание полей:
# - `id`: Автоинкрементируемый первичный ключ.
# - `user_id`: Внешний ключ, связывающий с таблицей пользователей (user).
# - `comment`: Необязательное текстовое поле для комментариев.
# - `full_amount`: Обязательное целочисленное поле, больше 0.
# - `invested_amount`: Сумма, распределенная по проектам, значение по умолчанию 0.
# - `fully_invested`: Булево значение, указывающее на то, полностью ли распределены деньги, по умолчанию `False`.
# - `create_date`: Дата создания пожертвования, автоматически устанавливается.
# - `close_date`: Дата закрытия пожертвования, автоматически устанавливается при полном распределении средств.
