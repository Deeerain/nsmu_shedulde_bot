from enum import Enum

from telegram import (
    Update, KeyboardButton, ReplyKeyboardMarkup)
from telegram.ext import ContextTypes, ConversationHandler

from bot.bot_instance import application, get_spec_keyboard, get_group_keyboard
from services.specialization import get_by_name
from services.group import get_group_by_name


class SubsButtons(Enum):
    SUBSCIBE: str = 'Подписаться'
    MY_SUBSCRIBES: str = 'Мои подписки'


class SubscribesCommandState(Enum):
    CHOISE_SPECIALIZATION = 1
    CHOISE_GROUP = 2


async def subscribes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton(SubsButtons.SUBSCIBE.value)],
        [KeyboardButton(SubsButtons.MY_SUBSCRIBES.value)]
    ]

    replay_marup = ReplyKeyboardMarkup(keyboard)

    await application.bot.send_message(update.message.chat_id, 'Меню подписок', reply_markup=replay_marup)


async def choise_specialization(update: Update, context: ContextTypes.DEFAULT_TYPE):
    replay_keyboard = ReplyKeyboardMarkup(
        get_spec_keyboard(keyboard_type=ReplyKeyboardMarkup))

    await application.bot.send_message(update.message.chat_id, "Ваша специализация", reply_markup=replay_keyboard)

    return SubscribesCommandState.CHOISE_SPECIALIZATION


async def ready_specialization(update: Update, context: ContextTypes.DEFAULT_TYPE):

    specialization = get_by_name(update.message.text)

    print(specialization)

    replay_keyboard = ReplyKeyboardMarkup(
        get_group_keyboard(specialization.specialization_id, ReplyKeyboardMarkup))

    context.user_data.setdefault(
        SubscribesCommandState.CHOISE_SPECIALIZATION, specialization)

    await application.bot.send_message(update.message.chat_id, f'Отлично, теперь выбери группу', reply_markup=replay_keyboard)

    return SubscribesCommandState.CHOISE_GROUP


async def ready_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group = get_group_by_name(update.message.text)

    keyboard = [
        [KeyboardButton('Подписаться')],
        [KeyboardButton('Отмена')],
    ]

    replay_keyboard = ReplyKeyboardMarkup(keyboard)

    context.user_data.setdefault(SubscribesCommandState.CHOISE_GROUP, group)

    await application.bot.send_message(update.message.chat_id, text='Отлично!', reply_markup=replay_keyboard)

    return ConversationHandler.END


async def subscribe_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await application.bot.send_message(update.message.chat_id, 'Отлично, вы подписались')

    return ConversationHandler.END
