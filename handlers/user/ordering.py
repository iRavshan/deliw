from aiogram import Router, F
from loader import bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from states.user_order import UserOrder
from aiogram.fsm.context import FSMContext
from typing import Any, Dict
from commands.default_commands import make_order
from keyboards.default.menu_for_user import auth_user_menu_markup
from data.repositories.user_repository import UserRepository
from data.repositories.order_repository import OrderRepository, Order

user_repository = UserRepository()
order_repository = OrderRepository()
router = Router()

@router.message(F.text == make_order)
async def start_order(message: Message, state: FSMContext) -> None:
    await state.set_state(UserOrder.numbers)
    await message.answer(f"Nechta suv buyurtma qilmoqchisiz?", 
                         reply_markup=ReplyKeyboardRemove())


@router.message(UserOrder.numbers)
async def get_numbers(message: Message, state: FSMContext) -> None:
    msg = message.text
    if(msg.isdigit()):
        if(int(msg) > 0):
            if(len(msg) < 6):
                data = await state.update_data(numbers=message.text)
                await message.answer(f"<b>✅ Buyurtmangiz qabul qilindi</b>", 
                                     reply_markup=auth_user_menu_markup())
                await get_data(message, data)
            else:
                await message.answer(f"<b>❕ Buyurtma soni maksimal 10 000 bo'lishi mumkin</b>")
        else:
            await message.answer(f"<b>❕ Buyurtma soni faqat 0 dan katta sonda bo'la oladi</b>")
    else:
        await message.answer(f"<b>❕ Buyurtma sonini faqat raqamlarda kiriting</b>")

async def get_data(message: Message, data: Dict[str, Any]) -> None:
    user = user_repository.find_by_id(message.from_user.id)
    new_order = Order(numbers=data["numbers"])
    new_order.user_id = user.tgId
    new_order = order_repository.create(new_order)
    await bot.send_message(chat_id="1919256193", text=f''' <b>📥 YANGI BUYURTMA</b>\n\n<b>Mijoz: </b><i>{user.firstname}</i>\n\n<b>Telefon raqam: </b>+{user.phone}\n\n<b>Buyurtma vaqti: </b>{new_order.created_at}\n\n<b>Buyurtma soni: </b>{new_order.numbers} ta\n\n@mumtaz_suv_bot''')
    await bot.send_location(chat_id="1919256193", latitude=user.latitude, longitude=user.longitude)




    
    