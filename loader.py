from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import pymongo

bot = Bot(token="6766715274:AAGRMYuQVlLDyA9g5GAn1pBMI5sgLWQMex0", parse_mode=ParseMode.HTML)
dp = Dispatcher()

db_client = pymongo.MongoClient("mongodb+srv://iRavshan:Qarshi-2002@cluster0.umrxpw4.mongodb.net/")
db = db_client["mumtaz_suv"]

users = db["users"]
orders = db["orders"]
