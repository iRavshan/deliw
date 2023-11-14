import sqlalchemy as orm
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import psycopg2

HOST = "viaduct.proxy.rlwy.net"
PORT = "58784"
USER = "postgres"
PASSWORD = "E-GG32f2A5BfF3DCfG-dG3D3*Ef6f-g4"
DB_NAME = "railway"
TOKEN = "6766715274:AAGRMYuQVlLDyA9g5GAn1pBMI5sgLWQMex0"

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

connection = f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
db_engine = orm.create_engine(connection)

