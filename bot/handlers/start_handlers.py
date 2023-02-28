from enum import Enum
import logging

from telegram import (Update, ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import ContextTypes, ConversationHandler

from bot.bot_instance import application, get_group_keyboard, get_spec_keyboard
from services import specialization
from services import group
from services import user
from services import subscribe
from db.models import User, Subscribe


logger = logging.getLogger(__name__)


class State(Enum):
    SPECIALIZATION = 1
    GROUP = 2


@user.get_user_decorator
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, *, user:  User) -> State:

    user_subscribes = subscribe.all_subscribes_by_user(user)

    if len(user_subscribes) >= 1:
        user_subscribe = user_subscribes[-1]

        return ConversationHandler.END

    keyboard = ReplyKeyboardMarkup(get_spec_keyboard(ReplyKeyboardMarkup))
    await application.bot.send_message(update.message.chat_id, text="Добро пожаловать в Бота")
    await application.bot.send_message(update.message.chat_id, text="Давай выберем вашу специализацию", reply_markup=keyboard)
    return State.SPECIALIZATION


async def choise_specialization(update: Update, context: ContextTypes.DEFAULT_TYPE) -> State:
    text = update.message.text

    if text:
        spec = specialization.get_by_name(text)

        context.user_data['spec'] = spec

        keyboard = ReplyKeyboardMarkup(get_group_keyboard(
            spec.specialization_id, ReplyKeyboardMarkup))

        await application.bot.send_message(update.message.chat_id, text=f"Ваша специализация: {spec.title}")
        await application.bot.send_message(update.message.chat_id, text=f"Отлично! Давай выберем вашу группу", reply_markup=keyboard)

        return State.GROUP


@user.get_user_decorator
async def choise_group(update: Update, context: ContextTypes.DEFAULT_TYPE, *, user: User):
    text = update.message.text
    choise_group = group.get_group_by_name(text)

    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton('Сохранить')],
        [KeyboardButton('Отмена')],
    ])

    await application.bot.send_message(update.message.chat_id, text=f"Ваша группа: {choise_group.title}")

    sub = subscribe.create_subscribe(user, choise_group)

    logger.info(f'New subscribe: {sub.subscribe_id}')

    context.user_data.clear()

    return ConversationHandler.END
