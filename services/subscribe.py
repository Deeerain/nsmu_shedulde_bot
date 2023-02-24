from db import Session
from db.models import User, Subscribe


def all_subscribes_by_user(user: User) -> list[Subscribe]:
    with Session() as s:
        return s.query(Subscribe).filter_by(user_id=user.user_id).all()
