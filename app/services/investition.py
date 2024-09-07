from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation


def close_obj(obj) -> None:
    """Закрывает объект.

    Устанавливает его как полностью инвестированный,
    сумма инвестиций равна сумме проекта,
    дата закрытия на момент закрытия.
    """
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def add_donations_to_project(
    charity_project: CharityProject, session: AsyncSession
) -> CharityProject:
    """Добавляет все доступные донаты в проект."""
    # available_donations = await donation_crud.get_open_obj_sorted(session)
    available_donations = await donation_crud.filter(
        session, fully_invested=False)

    if not available_donations:
        return charity_project

    for donation in available_donations:
        left_in_project = (
            charity_project.full_amount - charity_project.invested_amount
        )
        left_in_donation = donation.full_amount - donation.invested_amount

        if left_in_project <= 0:
            break

        if left_in_donation <= left_in_project:
            charity_project.invested_amount += left_in_donation
            close_obj(donation)
            if charity_project.full_amount == charity_project.invested_amount:
                close_obj(charity_project)
        else:
            charity_project.invested_amount += left_in_project
            donation.invested_amount += left_in_project

        session.add(donation)

    session.add(charity_project)
    await session.commit()
    await session.refresh(charity_project)

    return charity_project


async def distribute_donation(
    donation: Donation, session: AsyncSession
) -> Donation:
    """Распрделяет донат по всем открытм проектам."""
    charity_projects = await charity_project_crud.get_open_obj_sorted(session)
    # charity_projects = await charity_project_crud.filter(
    #     session, fully_invested=False)

    if not charity_projects:
        return donation

    for charity_project in charity_projects:
        if donation.full_amount == donation.invested_amount:
            close_obj(donation)
            break
        left_in_donation = donation.full_amount - donation.invested_amount
        left_in_project = (
            charity_project.full_amount - charity_project.invested_amount
        )

        if left_in_project > left_in_donation:
            charity_project.invested_amount += left_in_donation
            close_obj(donation)

        else:
            close_obj(charity_project)
            donation.invested_amount += left_in_project

        session.add(charity_project)

    session.add(donation)

    await session.commit()
    await session.refresh(donation)
    return donation


async def close_fully_invested(
    new_full_amount: int,
    charity_project: CharityProject,
    session: AsyncSession,
) -> CharityProject:
    """Закрывает проект, который набрал полную сумму."""
    if new_full_amount == charity_project.invested_amount:
        close_obj(charity_project)

        session.add(charity_project)
        await session.commit()
        await session.refresh(charity_project)

    return charity_project
