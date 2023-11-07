from aiogram import Router, F
from datetime import datetime
from loader import users, orders, bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from states.user_order import UserOrder
from aiogram.fsm.context import FSMContext
from typing import Any, Dict
from commands.default_commands import make_order
from keyboards.default.menu_for_user import auth_user_menu_markup

router = Router()

@router.message(F.text == make_order)
async def start_order(message: Message, state: FSMContext) -> None:
    await state.set_state(UserOrder.numbers)
    await message.answer(f"Nechta suv buyurtma qilmoqchisiz?", 
                         reply_markup=ReplyKeyboardRemove())


@router.message(UserOrder.numbers)
async def get_numbers(message: Message, state: FSMContext) -> None:
    data = await state.update_data(numbers=message.text)
    await message.answer(f"<b>✅ Buyurtmangiz qabul qilindi</b>", 
                         reply_markup=auth_user_menu_markup())
    await get_data(message, data)


async def get_data(message: Message, data: Dict[str, Any]) -> None:
    user = users.find_one({"tg_id": message.from_user.id})
    new_order = {
        "user_id": user["tg_id"],
        "created_at": datetime.now(),
        "numbers": data["numbers"]
    }
    orders.insert_one(new_order) 
    await bot.send_message(chat_id="1919256193", text=f''' <b>📥 YANGI BUYURTMA</b>\n\n<b>Mijoz: </b><i>{user["firstname"]}</i>\n\n<b>Telefon raqam: </b>{user["phone"]}\n\n<b>Manzil: </b>{user["address"]}\n\n<b>Buyurtma vaqti: </b>{new_order["created_at"].strftime("%m/%d/%Y, %H:%M")}\n\n<b>Buyurtma soni: </b>{new_order["numbers"]} ta\n\n@mumtaz_suv_bot''')




    
    