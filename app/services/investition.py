from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from datetime import datetime


async def add_donations_to_project(charity_project, session: AsyncSession):

    available_donations = await donation_crud.get_open_donations_sorted(
        session)

    for donation in available_donations:
        left_in_project = (
            charity_project.full_amount - charity_project.invested_amount)
        left_in_donation = donation.full_amount - donation.invested_amount

        if left_in_project <= 0:
            break

        if left_in_donation <= left_in_project:
            charity_project.invested_amount += left_in_donation
            donation.invested_amount += left_in_donation
            donation.fully_invested = True
            donation.close_date = datetime.now()
            if charity_project.full_amount == charity_project.invested_amount:
                charity_project.fully_invested = True
                charity_project.close_date = datetime.now()
        else:
            charity_project.invested_amount += left_in_project
            donation.invested_amount += left_in_project

        session.add(donation)

    session.add(charity_project)
    await session.commit()
    await session.refresh(charity_project)

    return charity_project


async def distribute_donation(donation, session):
    charity_projects = await charity_project_crud.get_open_projects_sorted(
        session)

    if not charity_projects:
        return donation

    for charity_project in charity_projects:
        if donation.full_amount == donation.invested_amount:
            donation.fully_invested = True
            donation.close_date = datetime.now()
            break
        left_in_donation = donation.full_amount - donation.invested_amount
        left_in_project = (
            charity_project.full_amount - charity_project.invested_amount)

        if left_in_project > left_in_donation:
            charity_project.invested_amount += left_in_donation
            donation.invested_amount += left_in_donation
            donation.close_date = datetime.now()
            donation.fully_invested = True

        else:
            charity_project.invested_amount += left_in_project
            charity_project.fully_invested = True
            charity_project.close_date = datetime.now()
            donation.invested_amount += left_in_project

        session.add(charity_project)

    session.add(donation)

    await session.commit()
    await session.refresh(donation)
    return donation


async def close_fully_invested(charity_project, session: AsyncSession):

    charity_project.fully_invested = True
    charity_project.close_date = datetime.now()

    session.add(charity_project)
    await session.commit()
    await session.refresh(charity_project)

    return charity_project