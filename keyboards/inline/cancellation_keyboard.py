from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from commands import inline_commands

def cancellation_markup() -> InlineKeyboardMarkup:
    inline_button = [InlineKeyboardButton(text=inline_commands.cancel, callback_data="cancel")]
    
    inline_keyboard = InlineKeyboardMarkup(keyboard=inline_button)
    
    return inline_keyboard