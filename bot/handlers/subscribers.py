from enum import Enum

from telegram import (
    Update, KeyboardButton, ReplyKeyboardMarkup)
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler

from bot.bot_instance import application, get_spec_keyboard


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
    # await update.message.edit_reply_markup(replay_marup)


async def choise_specialization(update: Update, context: ContextTypes.DEFAULT_TYPE):
    replay_keyboard = get_spec_keyboard(keyboard_type=ReplyKeyboardMarkup)

    await application.bot.send_message(update.message.chat_id, "Ваша специализация", reply_markup=replay_keyboard)

    return SubscribesCommandState.CHOISE_SPECIALIZATION


async def ready_specialization(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await application.bot.send_message(update.message.chat_id, f'Your choise: {update.message.text}')


async def subscribe_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


subscriber_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text(
        SubsButtons.SUBSCIBE.value), choise_specialization)],
    states={
        SubscribesCommandState.CHOISE_SPECIALIZATION: [MessageHandler(
            filters.ALL, ready_specialization)]
    },
    fallbacks=[]
)

application.add_handler(MessageHandler(
    filters.Text("Подписка"), subscribes))
application.add_handler(subscriber_conversation_handler)
