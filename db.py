from nsmu_parser import get_list, get_specs, get_groups
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, Session as DbSession


engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)

DeclarativeBase = declarative_base()
meta = MetaData()


def get_or_create(session: DbSession, model: any, **kwargs):
    with session as sess:
        instance = sess.query(model).filter_by(**kwargs).first()

        if instance:
            return instance

        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
