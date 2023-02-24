from sqlalchemy.orm import Session


def get_or_create(session: Session, model: any, **kwargs):
    with session as s:
        instance = s.query(model).filter_by(**kwargs).first()

        if instance:
            return instance

        instance = model(**kwargs)
        s.add(instance)
        s.commit()
        return instance
