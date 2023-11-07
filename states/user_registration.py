from aiogram.fsm.state import StatesGroup, State

class UserRegistrationState(StatesGroup):
    firstname = State()
    address = State()
    phone = State()