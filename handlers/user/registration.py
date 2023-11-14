from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
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
        await state.clear()
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
    if(message.content_type == ContentType.CONTACT):
        await state.update_data(phone=message.contact.phone_number)
        await state.set_state(UserRegistrationState.address)
        await message.answer(f"Manzilingiz", reply_markup=request_location.request_location())
    else:
        await message.answer(f"Iltimos telefon raqamingizni yuboring")


@router.message(UserRegistrationState.address)
async def get_address(message: Message, state: FSMContext) -> None:
    if(message.content_type == ContentType.LOCATION):
        await state.update_data(latitude=message.location.latitude)
        data = await state.update_data(longitude=message.location.longitude)
        await state.clear()
        await message.answer(text="Ro'yxatdan o'tish yakunlandi", 
                         reply_markup=auth_user_menu_markup())
        await get_data_and_create_user(message, data)
    else:
        await message.answer(text="Iltimos pastdagi tugma orqali manzilingizni yuboring")

async def get_data_and_create_user(message: Message, data: Dict[str, Any]) -> None:
    firstname = data["firstname"]
    phone = data["phone"]
    longitude = data["longitude"]
    latitude = data["latitude"]
    user = User(firstname=firstname, phone=phone, latitude=latitude, longitude=longitude)
    user_repo.update(message.from_user.id, user)