from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject


async def invest(new, crud_obj, session: AsyncSession):
    """Проводит операции инвестирования.

    Новый донат распределяет по всем открытым проектам.
    В новый проект добавляет все доступные донаты.
    """
    all_opened = await crud_obj.filter(session, fully_invested=False)

    if not all_opened:
        return new

    for opened in all_opened:
        if left(opened) >= left(new):
            opened.invested_amount += left(new)
            close(new)
            if left(opened) == left(new):
                close(opened)
            break
        else:
            new.invested_amount += left(opened)
            close(opened)

        session.add(opened)

    session.add(new)

    await session.commit()
    await session.refresh(new)
    return new


async def close_fully_invested(
    new_full_amount: int,
    charity_project: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    """Закрывает проект, который набрал полную сумму."""
    if new_full_amount == charity_project.invested_amount:
        close(charity_project)

        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)

    return charity_project


def left(obj) -> int:
    """Возвращает оставшуюся сумму инвестиций в проекте."""
    return obj.full_amount - obj.invested_amount


def close(obj) -> None:
    """Закрывает проект как полностью инвестированный."""
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
