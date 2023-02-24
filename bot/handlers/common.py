import logging
from typing import Sequence

from telegram import (Update, InlineKeyboardButton,
                      InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import (Application, CommandHandler,
                          ContextTypes, filters, CallbackQueryHandler, MessageHandler,
                          ConversationHandler)

import services
import models
from bot.bot_instance import get_spec_keyboard, get_group_keyboard, application


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
