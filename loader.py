from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import pymongo

bot = Bot(token="6838467582:AAFSO4HfTjwR3huucLhLdIjP5TQ1K6aN2E4", parse_mode=ParseMode.HTML)
dp = Dispatcher()

db_client = pymongo.MongoClient("mongodb+srv://iRavshan:Qarshi-2002@cluster0.umrxpw4.mongodb.net/")
db = db_client["mumtaz_suv"]

users = db["users"]
orders = db["orders"]
