from db import Session
from db.models import Group


def create_group(title: str, link: int, spec_id: int) -> Group | None:
    with Session() as s:
        new_group = Group(title=title, link=link, specialization_id=spec_id)

        s.add(new_group)
        s.commit()

        return new_group


def all_groups() -> list[Group] | None:

    with Session() as s:

        return s.query(Group).all()


def all_group_by_spec(spec_id: int):
    with Session() as s:
        return s.query(Group).filter_by(specialization_id=spec_id).all()


def get_group_by_id(id: int) -> Group | None:

    with Session() as s:
        return s.query(Group).filter_by(group_id=id).first()
