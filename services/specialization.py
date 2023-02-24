from db import Session
from db.models import Specialization, Group


def create_spec(title: str, link: int) -> Specialization | None:

    with Session() as s:
        new_specialization = Specialization(title=title, link=link)

        s.add(new_specialization)

        s.commit()

        return new_specialization


def all_specs() -> list[Specialization] | None:

    with Session() as s:

        specializations = s.query(Specialization).all()
        return specializations


def all_group_by_spec(spec_id: int) -> list[Group]:
    with Session() as s:
        return s.query(Group).filter_by(specialization_id=spec_id)
