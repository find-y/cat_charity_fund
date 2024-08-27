from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.db import Base


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=func.now(), nullable=False)
    # может вынести в базовый класс?
    close_date = Column(DateTime)

# Описание требований:
# - `name` должен быть уникальным и длиной от 1 до 100 символов.
# - `description` обязательно и должно содержать не менее одного символа.
# - `full_amount` должно быть больше 0.
# - `invested_amount` по умолчанию 0.
# - `fully_invested` по умолчанию False.
# - `create_date` устанавливается автоматически при создании проекта.
# - `close_date` устанавливается при закрытии проекта.
