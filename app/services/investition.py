from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from sqlalchemy.exc import SQLAlchemyError


async def distribute_donation(donation, session):
    left_in_donation = donation.full_amount - donation.invested_amount
    charity_projects = await charity_project_crud.get_open_projects_sorted(session)
    if not charity_projects:
        return
    else:
        proj_number = 0
        while left_in_donation > 0 and proj_number < len(charity_projects):
            left_in_donation = donation.full_amount - donation.invested_amount
            charity_project = charity_projects[proj_number]
            left_in_project = charity_project.full_amount - charity_project.invested_amount
            if left_in_project >= left_in_donation:
                current_invest = left_in_donation
                charity_project.invested_amount += current_invest
                donation.invested_amount += current_invest
                if donation.full_amount == donation.invested_amount:  # контрольная проверка, можно убрать
                    donation.close_date = func.now()
                    donation.fully_invested = True
                # if left_in_project == left_in_donation:
                if charity_project.fully_invested == charity_project.invested_amount:  # условие, если выше было равно. нельяз убрать
                    charity_project.fully_invested = True
                    charity_project.close_date = func.now()
            else:
                current_invest = left_in_project
                charity_project.invested_amount += current_invest
                charity_project.fully_invested = True
                charity_project.close_date = func.now()
                donation.invested_amount += current_invest
            proj_number += 1

            session.add(charity_project)

        session.add(donation)

        # for project in charity_projects:
        #     session.add(project)
        await session.commit()
        await session.refresh(donation)
    return donation

    # except SQLAlchemyError as e:
    #     await session.rollback()
    #     print(f"Database error occurred: {e}")
    #     raise


async def add_donations_to_project(charity_project, session: AsyncSession):

    available_donations = await donation_crud.get_open_donations_sorted(session)
    
    for donation in available_donations:
        
        left_in_project = charity_project.full_amount - charity_project.invested_amount
        left_in_donation = donation.full_amount - donation.invested_amount

        if left_in_project <= 0:
            break

        if left_in_donation <= left_in_project:
            charity_project.invested_amount += left_in_donation
            donation.invested_amount += left_in_donation
            if donation.full_amount == donation.invested_amount:  # контрольная проверка, можно убрать
                donation.fully_invested = True
                donation.close_date = func.now()
            if charity_project.full_amount == charity_project.invested_amount:  # условие, если выше было равно. нельяз убрать
                charity_project.fully_invested = True
                charity_project.close_date = func.now()
        else:
            charity_project.invested_amount += left_in_project
            donation.invested_amount += left_in_project

        session.add(donation)

    # for donation in available_donations:
    #     session.add(donation)

    session.add(charity_project)
    await session.commit()

    await session.refresh(charity_project)

    # charity_project = await charity_project_crud.get(charity_project.id, session)

    return charity_project