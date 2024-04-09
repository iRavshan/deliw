import os
import psycopg2
import sqlalchemy as orm
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from data.models import Base

load_dotenv()

HOST = os.environ.get('DB_HOST')
PORT = os.environ.get('DB_PORT')
USER = os.environ.get('DB_USER')
PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
TOKEN = os.environ.get('BOT_TOKEN')

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

connection = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
db_engine = orm.create_engine(connection)

def create_tables():
    Base.metadata.create_all(bind=db_engine)

