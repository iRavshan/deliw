from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from commands import inline_commands

def cancellation_markup() -> InlineKeyboardMarkup:
    inline_buttons = [
        [
            InlineKeyboardButton(text=inline_commands.cancel, callback_data="cancel")
        ]
    ]
    
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
    
    return inline_keyboard