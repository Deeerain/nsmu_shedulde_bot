from telegram import Update

from db import Session
from db.models import User
from services.common import get_or_create


def get_or_create_user(telegram_chat_id: int, telegram_user_id: int) -> User:
    with Session() as s:
        user = get_or_create(
            s, User, telegram_chat_id=telegram_chat_id, telegram_user_id=telegram_user_id)

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
