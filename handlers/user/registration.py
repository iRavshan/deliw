from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from typing import Any, Dict
from states.user_registration import UserRegistrationState
from commands.slash_commands import registration
from keyboards.default.menu_for_user import user_menu_markup, auth_user_menu_markup
from keyboards.default import request_contact, request_location
from data.repositories.user_repository import UserRepository
from data.models import User

router = Router()
user_repo = UserRepository()

@router.message(F.text, Command(registration))
async def start_registration(message: Message, state: FSMContext) -> None:
    ex_user = user_repo.find_by_id(message.from_user.id)
    if(ex_user.is_registered is not False):
        await message.answer(f"Siz ro'yxatdan o'tgansiz. Marhamat pastdagi tugma orqali buyurtma bering 👇🏻", 
                             reply_markup=auth_user_menu_markup())
    else:
        await state.set_state(UserRegistrationState.firstname)
        await message.answer(f"Ismingizni yozing",
                             reply_markup=ReplyKeyboardRemove())



@router.message(UserRegistrationState.firstname)
async def get_name(message: Message, state: FSMContext) -> None:
    await state.update_data(firstname=message.text)
    await state.set_state(UserRegistrationState.phone)
    await message.answer(f"Telefon raqamingiz", reply_markup=request_contact.request_contact())


@router.message(UserRegistrationState.phone)
async def get_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(UserRegistrationState.address)
    await message.answer(f"Manzilingiz", reply_markup=request_location.request_location())


@router.message(UserRegistrationState.address)
async def get_address(message: Message, state: FSMContext) -> None:
    data = await state.update_data(address=message.location)
    await state.clear()
    firstname = data["firstname"]
    address = data["address"]
    phone = data["phone"]
    await message.answer(text="Ro'yxatdan o'tish yakunlandi", 
                         reply_markup=auth_user_menu_markup())
    await get_data_and_create_user(message, data)


async def get_data_and_create_user(message: Message, data: Dict[str, Any]) -> None:
    firstname = data["firstname"]
    address = data["address"]
    phone = data["phone"]
    user = User()
    user_repo.create(new_user)