import logging
from typing import Sequence

from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton)
from telegram.ext import Application

from services.group import all_group_by_spec
from services.specialization import all_specs


TOKEN = '6098297978:AAGr3lmVE9ogwEcS06TBEQKI7ZC7SCZy5Zs'

logger = logging.getLogger(__name__)

application = Application.builder().token(TOKEN).build()


def get_spec_keyboard(keyboard_type: InlineKeyboardMarkup | ReplyKeyboardMarkup) -> list[Sequence[Sequence[InlineKeyboardButton]]]:
    """Получение клавиатуры со списком специализаций"""
    keyboard = []
    keyboard_button_type = KeyboardButton if keyboard_type == ReplyKeyboardMarkup else InlineKeyboardButton

    for spec in all_specs():
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

    for group in all_group_by_spec(spec):

        button_data: dict[str, str] = {}
        button_data['text'] = group.title

        if keyboard_button_type == InlineKeyboardButton:
            button_data['text'] = group.title
            button_data['callback_data'] = str(f'group:{group.group_id}')

        keyboard.append([keyboard_button_type(**button_data)])

    return keyboard
