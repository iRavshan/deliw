from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from commands import keyboard_commands

def request_location() -> ReplyKeyboardMarkup:
    kb = [[KeyboardButton(text=keyboard_commands.request_location, request_location=True)]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, 
                                   resize_keyboard=True, 
                                   one_time_keyboard=True)
    return keyboard