from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject


# async def invest(new,
#                  crud_obj,
#                  session: AsyncSession):
#     """Проводит операции инвестирования.

#     Новый донат распределяет по всем открытым проектам.
#     В новый проект добавляет все доступные донаты.
#     """
#     all_opened = await crud_obj.filter(session, fully_invested=False)

#     if not all_opened:
#         return new

#     for opened in all_opened:
#         if opened.left() >= new.left():
#             opened.invested_amount += new.left()
#             new.close()
#             if opened.left() == new.left():
#                 opened.close()
#             break
#         else:
#             new.invested_amount += opened.left()
#             opened.close()

#         session.add(opened)

#     session.add(new)

#     await session.commit()
#     await session.refresh(new)
#     return new


async def invest(new,
                 crud_obj,
                 session: AsyncSession):
    """Проводит операции инвестирования.

    Новый донат распределяет по всем открытым проектам.
    В новый проект добавляет все доступные донаты.
    """
    all_opened = await crud_obj.filter(session, fully_invested=False)

    if not all_opened:
        return new

    for opened in all_opened:
        if crud_obj.left(opened) >= crud_obj.left(new):
            opened.invested_amount += crud_obj.left(new)
            new.close()
            if crud_obj.left(opened) == crud_obj.left(new):
                crud_obj.close(opened)
            break
        else:
            new.invested_amount += crud_obj.left(opened)
            crud_obj.close(opened)

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
