from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)

DeclarativeBase = declarative_base()
meta = MetaData()
