from datetime import date

from telegram import Update

from db import Session, get_or_create
from nsmu_parser import get_list
from models import Specialization, Group, User, Subscribe


def all_groups() -> list[Group] | None:

    with Session() as session:

        return session.query(Group).all()


def all_specs() -> list[Specialization] | None:

    with Session() as session:

        specializations = session.query(Specialization).all()
        return specializations


def all_subscribes_by_user(user: User) -> list[Subscribe]:
    with Session() as session:
        return session.query(Subscribe).filter_by(user_id=user.user_id).all()


def get_group_by_id(id: int) -> Group | None:

    with Session() as session:
        return session.query(Group).filter_by(group_id=id).first()


def all_group_by_spec(spec_id: int) -> list[Group]:
    with Session() as session:
        return session.query(Group).filter_by(specialization_id=spec_id)


def create_group(title: str, link: int, spec_id: int) -> Group | None:
    with Session() as session:
        new_group = Group(title=title, link=link, specialization_id=spec_id)

        session.add(new_group)
        session.commit()

        return new_group


def create_spec(title: str, link: int) -> Specialization | None:

    with Session() as session:
        new_specialization = Specialization(title=title, link=link)

        session.add(new_specialization)

        session.commit()

        return new_specialization


def shedulde_by_group(link: str, shedulde_time: str):
    today_date = date.today()
    tomoroww_date = date(today_date.year, today_date.month, today_date.day + 1)

    if shedulde_time == 'today':
        return get_list(today_date, link)

    if shedulde_time == 'tomorrow':
        return get_list(tomoroww_date, link)


def get_or_create_user(telegram_chat_id: int, telegram_user_id: int) -> User:
    with Session() as session:
        user = get_or_create(
            session, User, telegram_chat_id=telegram_chat_id, telegram_user_id=telegram_user_id)

        return user


def get_user_decorator(func: callable):
    async def wrapper(*args, **kwargs):
        user = None

        for arg in args:
            if isinstance(arg, Update):
                message = arg.message or arg.callback_query.message
                user = get_or_create_user(
                    message.chat.id, message.from_user.id)

        return await func(*args, user=user, **kwargs)
    return wrapper
