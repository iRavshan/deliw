from loader import bot
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.methods.edit_message_reply_markup import EditMessageReplyMarkup
from aiogram.types import Message, ContentType, CallbackQuery, ReplyKeyboardRemove
from commands.keyboard_commands import make_order as kb_make_order
from commands.menu_commands import make_order as menu_make_order
from data.models import User
from data.repositories.user_repository import UserRepository
from data.repositories.order_repository import OrderRepository, Order
from keyboards.default import request_contact, request_location
from keyboards.default.keyboard_for_user import user_menu_markup
from keyboards.inline.cancellation_keyboard import cancellation_markup
from states.user_order import UserOrder
from states.user_registration import UserRegistrationState
from typing import Any, Dict


user_repository = UserRepository()
order_repository = OrderRepository()
router = Router()

#-------- /MAKE AN ORDER -------#
@router.message(F.text == kb_make_order)
async def start_order(message: Message, state: FSMContext) -> None:
    await start_order(message, state)
  
    
@router.message(Command(menu_make_order))
async def start_order(message: Message, state: FSMContext) -> None:
    await start_order(message, state)


async def start_order(message: Message, state: FSMContext)-> None:
    await state.clear()
    user = user_repository.find_by_id(message.from_user.id)
    if(not user.is_registered):
        await start_registration(message, state)
    else:
        await state.set_state(UserOrder.numbers)
        await message.answer(f"Nechta suv buyurtma qilmoqchisiz?", 
                            reply_markup=cancellation_markup())


@router.message(UserOrder.numbers)
async def get_numbers(message: Message, state: FSMContext) -> None:
    msg = message.text
    if(msg.isdigit()):
        if(int(msg) > 0):
            if(len(msg) < 6):
                data = await state.update_data(numbers=message.text)
                await state.clear()
                await message.answer(f"<b>✅ Buyurtmangiz qabul qilindi</b>\n\n<i>Xaridingiz uchun tashakkur. Sizdek mijozlarga xizmat ko'rsatishdan mamnunmiz 🤝</i>", 
                                     reply_markup=user_menu_markup())
                await get_data_and_make_order(message, data)
            else:
                await message.answer(f"<b>❕ Buyurtma soni maksimal 10 000 bo'lishi mumkin</b>")
        else:
            await message.answer(f"<b>❕ Buyurtma soni faqat 0 dan katta sonda bo'la oladi</b>")
    else:
        await message.answer(f"<b>❕ Buyurtma sonini faqat raqamlarda kiriting</b>")


async def get_data_and_make_order(message: Message, data: Dict[str, Any]) -> None:
    user = user_repository.find_by_id(message.from_user.id)
    new_order = Order(numbers=data["numbers"])
    new_order.user_id = user.tgId
    new_order = order_repository.create(new_order)
    admins = ["5719584090", "1919256193", "806335725"]
    for i in range(0, len(admins)):
        await bot.send_message(chat_id=admins[i], text=f''' <b>📥 YANGI BUYURTMA</b>\n\n<b>Mijoz: </b><i>{user.firstname}</i>\n\n<b>Telefon raqam: </b>{user.phone}\n\n<b>Buyurtma vaqti: </b>{new_order.created_at}\n\n<b>Buyurtma soni: </b>{new_order.numbers} ta\n\n@zamin_water_bot''')
        await bot.send_location(chat_id=admins[i], latitude=user.latitude, longitude=user.longitude)


#-------- /REGISTRATION -------#
async def start_registration(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(UserRegistrationState.firstname)
    await message.answer(f"Ismingizni yozing", reply_markup=ReplyKeyboardRemove())


@router.message(UserRegistrationState.firstname)
async def get_name(message: Message, state: FSMContext) -> None:
    if(message.text.isalpha()):
        await state.update_data(firstname=message.text)
        await state.set_state(UserRegistrationState.phone)
        await message.answer(f"Telefon raqamingiz", reply_markup=request_contact.request_contact())
    else:
        await message.answer(f"Iltimos ismingizni faqat harflardan foydalangan holda kiriting")


@router.message(UserRegistrationState.phone)
async def get_phone(message: Message, state: FSMContext) -> None:
    if(message.content_type == ContentType.CONTACT):
        await state.update_data(phone=message.contact.phone_number)
        await state.set_state(UserRegistrationState.address)
        await message.answer(f"Manzilingiz", reply_markup=request_location.request_location())
    elif(message.content_type == ContentType.TEXT and len(message.text) > 8):
        await state.update_data(phone=message.text)
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
        await get_data_and_create_user(message, data)
        await start_order(message, state)
    else:
        await message.answer(text="Iltimos pastdagi «📍Manzilimni yuborish» tugmasi orqali manzilingizni yuboring")


async def get_data_and_create_user(message: Message, data: Dict[str, Any]) -> None:
    firstname = data["firstname"]
    phone = data["phone"]
    longitude = data["longitude"]
    latitude = data["latitude"]
    user = User(firstname=firstname, phone=phone, latitude=latitude, longitude=longitude)
    user_repository.update(message.from_user.id, user)
    

@router.callback_query(F.data == 'cancel')
async def cancel_action(query: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await query.bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, inline_message_id=query.inline_message_id, reply_markup=None)
    await query.bot.edit_message_text(text = f"Amal bekor qilindi 🛑", chat_id=query.message.chat.id, message_id=query.message.message_id, inline_message_id=query.inline_message_id, reply_markup=None)
    await query.answer(f"Amal bekor qilindi 🛑", reply_markup=None)
