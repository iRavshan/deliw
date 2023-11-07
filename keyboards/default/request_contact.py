from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from commands import default_commands

def request_contact() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text=default_commands.request_contact, request_contact=True)]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, 
                                   resize_keyboard=True, 
                                   one_time_keyboard=True)
    return keyboard