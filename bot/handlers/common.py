import logging

from telegram import (Update,
                      InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import ContextTypes

from services.user import get_user_decorator
from services.group import get_group_by_id
from services.shedulde import shedulde_by_group
import db.models as models
from bot.bot_instance import get_spec_keyboard, get_group_keyboard, application


@get_user_decorator
async def shedulde_today(update: Update, context: ContextTypes.DEFAULT_TYPE, *, user: models.User):
    logging.info('Shedulde today messgae handler')

    replay_markup = InlineKeyboardMarkup(
        get_spec_keyboard(InlineKeyboardMarkup))

    context.user_data['s_date'] = 'today'

    await update.message.reply_text(f'Выбери специализацию:',
                                    reply_markup=replay_markup)


@get_user_decorator
async def shedulde_tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE, *, user: models.User):
    logging.info('Welcome messgae handler')

    replay_markup = InlineKeyboardMarkup(
        get_spec_keyboard(InlineKeyboardMarkup))

    context.user_data['s_date'] = 'tomorrow'

    await update.message.reply_text(f'Выбери специализацию:',
                                    reply_markup=replay_markup)


@get_user_decorator
async def button(update: Update, contex: ContextTypes.DEFAULT_TYPE, *, user: models.User):
    type, data = update.callback_query.data.split(':')
    shedulde_time = contex.user_data.get('s_date', 'today')

    if type == 'spec':

        replay_markup = InlineKeyboardMarkup(
            get_group_keyboard(int(data), InlineKeyboardMarkup))

        await update.callback_query.edit_message_text('Выбор группы:')
        await update.callback_query.edit_message_reply_markup(replay_markup)

    if type == 'group':
        group = get_group_by_id(int(data))

        shedulde_text = '\n\n'.join(
            [shedulde.text for shedulde in shedulde_by_group(group.link, shedulde_time)])

        if shedulde_text:
            await update.callback_query.edit_message_text(shedulde_text, parse_mode='html')
            return

        await update.callback_query.edit_message_text('На сегодня нет раписания')
