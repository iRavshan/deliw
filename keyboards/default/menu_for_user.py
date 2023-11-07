from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from commands import default_commands

def auth_user_menu_markup() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=default_commands.make_order)],
        [
            KeyboardButton(text=default_commands.contact),
            KeyboardButton(text=default_commands.about)
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, 
                                   resize_keyboard=True, 
                                   one_time_keyboard=True)
    return keyboard


def user_menu_markup() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=default_commands.contact),
            KeyboardButton(text=default_commands.about)
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, 
                                   resize_keyboard=True, 
                                   one_time_keyboard=True)
    return keyboard