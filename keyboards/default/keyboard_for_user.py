from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from commands import keyboard_commands

def user_menu_markup() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=keyboard_commands.make_order),
            KeyboardButton(text=keyboard_commands.active_orders)
        ],
        [
            KeyboardButton(text=keyboard_commands.contact),
            KeyboardButton(text=keyboard_commands.about)
        ],
        [ 
            KeyboardButton(text=keyboard_commands.help)
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, 
                                   resize_keyboard=True, 
                                   one_time_keyboard=True)
    return keyboard