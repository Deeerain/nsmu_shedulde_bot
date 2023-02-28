from db import Session
from db.models import User, Subscribe, Group


def all_subscribes_by_user(user: User) -> list[Subscribe]:
    with Session() as s:
        return s.query(Subscribe).filter_by(user_id=user.user_id).all()


def create_subscribe(user: User, group: Group) -> Subscribe:
    with Session() as s:

        subscribe = Subscribe()
        subscribe.group_id = group.group_id
        subscribe.user_id = user.user_id

        s.add(subscribe)
        s.commit()

        return subscribe
