import logging
from typing import Sequence

from telegram import (Update, InlineKeyboardButton,
                      InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import (Application, CommandHandler,
                          ContextTypes, filters, CallbackQueryHandler, MessageHandler,
                          ConversationHandler)

import services
import models

from handlers import *


TOKEN = '6098297978:AAGr3lmVE9ogwEcS06TBEQKI7ZC7SCZy5Zs'

logger = logging.getLogger(__name__)

application = Application.builder().token(TOKEN).build()


def get_spec_keyboard(keyboard_type: InlineKeyboardMarkup | ReplyKeyboardMarkup) -> list[Sequence[Sequence[InlineKeyboardButton]]]:
    """Получение клавиатуры со списком специализаций"""
    keyboard = []
    keyboard_button_type = KeyboardButton if keyboard_type == ReplyKeyboardMarkup else InlineKeyboardButton

    for spec in services.all_specs():
        button_data: dict[str, str] = {}

        button_data['text'] = spec.title

        if keyboard_button_type == InlineKeyboardButton:
            button_data['callback_data'] = str(
                f"spec:{spec.specialization_id}")

        button = keyboard_button_type(**button_data)

        keyboard.append([button])

    return keyboard


def get_group_keyboard(spec: int, keyboard_type: InlineKeyboardMarkup | ReplyKeyboardMarkup) -> list[Sequence[Sequence[InlineKeyboardButton]]]:
    """Получение клавиатуры со списком групп"""
    keyboard = []
    keyboard_button_type = KeyboardButton if keyboard_type == ReplyKeyboardMarkup else InlineKeyboardButton

    for group in services.all_group_by_spec(spec):

        button_data: dict[str, str] = {}
        button_data['text'] = group.title

        if keyboard_button_type == InlineKeyboardButton:
            button_data['text'] = group.title
            button_data['callback_data'] = str(f'group:{group.group_id}')

        keyboard.append([keyboard_button_type(**button_data)])

    return keyboard


@services.get_user_decorator
async def wlecome(update: Update, context: ContextTypes.DEFAULT_TYPE, *, user: models.User):
    logging.info('Welcome messgae handler')

    keboard = [
        [KeyboardButton('Расписание (Сегодня)')],
        [KeyboardButton('Расписание (Завтра)')],
        [KeyboardButton('Подписка')],
    ]
    replay_markup = ReplyKeyboardMarkup(keboard)
    text = f'Добро пожаловать {update.message.from_user.full_name}'

    await application.bot.send_message(update.message.chat_id, text, reply_markup=replay_markup)


@services.get_user_decorator
async def shedulde_today(update: Update, context: ContextTypes.DEFAULT_TYPE, *, user: models.User):
    logging.info('Shedulde today messgae handler')

    replay_markup = InlineKeyboardMarkup(
        get_spec_keyboard(InlineKeyboardMarkup))

    await update.message.reply_text(f'Выбери специализацию:',
                                    reply_markup=replay_markup)


@services.get_user_decorator
async def shedulde_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE, *, user: models.User):
    logging.info('Welcome messgae handler')

    replay_markup = InlineKeyboardMarkup(
        get_spec_keyboard(InlineKeyboardMarkup))

    await update.message.reply_text(f'Выбери специализацию:',
                                    reply_markup=replay_markup)


@services.get_user_decorator
async def button(update: Update, contex: ContextTypes.DEFAULT_TYPE, *, user: models.User):
    type, data = update.callback_query.data.split(':')
    shedulde_time = contex.user_data.get('shedulde_time', 'today')

    if type == 'spec':

        replay_markup = InlineKeyboardMarkup(
            get_group_keyboard(int(data), InlineKeyboardMarkup))

        await update.callback_query.edit_message_text('Выбор группы:')
        await update.callback_query.edit_message_reply_markup(replay_markup)

    if type == 'group':
        group = services.get_group_by_id(int(data))

        shedulde_text = '\n\n'.join(
            [shedulde.text for shedulde in services.shedulde_by_group(group.link, shedulde_time)])

        if shedulde_text:
            await update.callback_query.edit_message_text(shedulde_text, parse_mode='html')
            return

        await update.callback_query.edit_message_text('На сегодня нет раписания')


application.add_handler(CommandHandler('start', wlecome))


application.add_handler(MessageHandler(
    filters.Text('Расписание (Сегодня)'), shedulde_tomorrow))
application.add_handler(MessageHandler(
    filters.Text('Расписание (Сегодня)'), shedulde_tomorrow))

application.add_handler(CallbackQueryHandler(button))
