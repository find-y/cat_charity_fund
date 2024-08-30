from sqlalchemy.sql import func
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud
from sqlalchemy.exc import SQLAlchemyError


async def distribute_donation(donation_id, session):
    # получили новый pydantic объект donation
    donation = await donation_crud.get(donation_id, session)
    left_in_donation = donation.full_amount - donation.invested_amount
    # получаем список открытых проектов, отсортированный по дате создания
    charity_projects = await charity_project_crud.get_open_projects_sorted(session)
    if not charity_projects:
        return
    else:
        # берем самый старый последний открытый проект
        proj_number = 0
        while left_in_donation > 0 and proj_number < len(charity_projects):
            # в донате: получаем сколько осталось для вложений
            left_in_donation = donation.full_amount - donation.invested_amount
            charity_project = charity_projects[proj_number]
            # в проекте, получаем сколько еще осталось для вложений:
            left_in_project = charity_project.full_amount - charity_project.invested_amount
            if left_in_project >= left_in_donation:
                current_invest = left_in_donation
                charity_project.invested_amount += current_invest
                donation.invested_amount += current_invest
                donation.close_date = func.now()
                donation.fully_invested = True
            else:
                current_invest = left_in_project
                charity_project.invested_amount += current_invest
                charity_project.fully_invested = True
                charity_project.close_date = func.now()
                donation.invested_amount += current_invest
            proj_number += 1

        session.add(donation)

        for project in charity_projects:
            session.add(project)
        await session.commit()
    return

    # except SQLAlchemyError as e:
    #     await session.rollback()
    #     print(f"Database error occurred: {e}")
    #     raise