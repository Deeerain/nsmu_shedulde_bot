from sqlalchemy import (
    Column, Integer, Text, ForeignKey)
from db.connection import DeclarativeBase


class User(DeclarativeBase):
    """Таблица пользователя"""
    __tablename__ = 'user'

    user_id = Column('id', Integer, primary_key=True)
    telegram_chat_id = Column(Integer)
    telegram_user_id = Column(Integer)


class Specialization(DeclarativeBase):
    """Таблица специализации"""
    __tablename__ = 'specialization'

    specialization_id = Column('id', Integer, primary_key=True)
    title = Column(Text)
    link = Column(Text)


class Group(DeclarativeBase):
    """Таблица группы"""
    __tablename__ = 'group'

    group_id = Column('id', Integer, primary_key=True)
    title = Column(Text)
    link = Column(Text)
    specialization_id = Column(Integer, ForeignKey(
        Specialization.specialization_id))


class Subscribe(DeclarativeBase):
    """Таблица подписки"""
    __tablename__ = 'subscribe'

    subscribe_id = Column('id', Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE'))
    group_id = Column(ForeignKey('group.id', ondelete='CASCADE'))
