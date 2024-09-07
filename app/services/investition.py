from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation


# def close_obj(obj) -> None:
#     """Закрывает объект.

#     Устанавливает его как полностью инвестированный,
#     сумма инвестиций равна сумме проекта,
#     дата закрытия на момент закрытия.
#     """
#     obj.invested_amount = obj.full_amount
#     obj.fully_invested = True
#     obj.close_date = datetime.now()


# async def invest(new, crud_obj, session: AsyncSession):
#     """Проводит операции инвестирования.

#     Новый донат распределяет по всем открытым проектам.
#     В новый проект добавляет все доступные донаты.
#     """
#     all_opened = await crud_obj.filter(session, fully_invested=False)

#     if not all_opened:
#         return new

#     for opened in all_opened:
#         if left(opened) >= left(new):
#             opened.invested_amount += left(new)
#             close_obj(new)
#             if left(opened) == left(new):
#                 close_obj(opened)
#             break
#         else:
#             new.invested_amount += left(opened)
#             close_obj(opened)

#         session.add(opened)

#     session.add(new)

#     await session.commit()
#     await session.refresh(new)
#     return new


# def left(obj):
#     """Возвращает оставшуюся сумму инвестиций в объекте."""
#     return obj.full_amount - obj.invested_amount


async def invest(new, crud_obj, session: AsyncSession):
    """Проводит операции инвестирования.

    Новый донат распределяет по всем открытым проектам.
    В новый проект добавляет все доступные донаты.
    """
    all_opened = await crud_obj.filter(session, fully_invested=False)

    if not all_opened:
        return new

    for opened in all_opened:
        if opened.left() >= new.left():
            opened.invested_amount += new.left()
            new.close()
            if opened.left() == new.left():
                opened.close()
            break
        else:
            new.invested_amount += opened.left()
            opened.close()

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
        charity_project.close()

        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)

    return charity_project
