from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from data.models import create_engine
import psycopg2

TOKEN = "6766715274:AAGRMYuQVlLDyA9g5GAn1pBMI5sgLWQMex0"

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

create_engine()

