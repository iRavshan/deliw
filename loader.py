from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import psycopg2

bot = Bot(token="6766715274:AAGRMYuQVlLDyA9g5GAn1pBMI5sgLWQMex0", parse_mode=ParseMode.HTML)
dp = Dispatcher()

con = psycopg2.connect(
    database="osontaksi",
    user="postgres",
    password="Qarshi-2002",
    host="localhost",
    port= '5432'
)

db = con.cursor()
