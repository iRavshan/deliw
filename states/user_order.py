from aiogram.fsm.state import StatesGroup, State

class UserOrder(StatesGroup):
    numbers = State()