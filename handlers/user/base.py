from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from commands.menu_commands import aloqa, info, my_orders
from commands.keyboard_commands import contact, about, active_orders, make_order
from keyboards.default.keyboard_for_user import user_menu_markup
from data.repositories.user_repository import UserRepository
from data.repositories.order_repository import OrderRepository
from data.models import User

router = Router()
user_repository = UserRepository()
order_repository = OrderRepository()
 

#-------- /START -------#
@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await clear_state(state)
    user_id = message.from_user.id
    ex_user = user_repository.find_by_id(user_id)
    if(ex_user is None):
        new_user = User(tgId=user_id)
        user_repository.create(new_user)
    
    await message.answer("Assalomu alaykum!\n\nZamin Water - tabiiy buloq suvi", reply_markup=user_menu_markup()) 


#-------- /INFO -------#
@router.message(F.text == about)
async def command_info_button(message: Message) -> None:
    await send_info(message)
    
@router.message(Command(info))
async def command_info_menu(message: Message) -> None:
    await send_info(message)

async def send_info(message: Message, state: FSMContext):
    await clear_state()
    await message.answer("<b>Zamin Water - tabiiy ichimlik suvi</b>\n\n💠 Tabiiy tog' suvi\n💠 10 bosqichli filtrda tozalangan\n💠 Uyingiz va ofisingiz uchun eng ma'qul\n🚗 Yetkazib berish mutlaqo <b>BEPUL</b>\n\n<b>💎 19 litr - 10.000 so'm</b>\n\n@zamin_water_bot orqali oson buyurtma bering")


#-------- /ALOQA -------#
@router.message(F.text == contact)
async def command_contact_button(message: Message) -> None:
    await send_contact(message)

@router.message(Command(aloqa))
async def command_contact_menu(message: Message) -> None:
    await send_contact(message)

async def send_contact(message: Message, state: FSMContext):
    await clear_state()
    await message.answer("<b>Barcha viloyatlar uchun aloqa telefonlari:</b>\n\n📞 +998996740440\n\n📞 +998993710440")


#-------- /Buyurtmalarim -------#
@router.message(F.text == active_orders)
async def command_orders_button(message: Message) -> None:
    await get_active_orders(message)


@router.message(Command(my_orders))
async def command_orders_menu(message: Message) -> None:
    await get_active_orders(message)


async def get_active_orders(message: Message, state: FSMContext):
    await clear_state()
    user = user_repository.find_by_id(message.from_user.id)
    
    if(user is None):
        await message.answer(f"Siz hali buyurtma bermagansiz. Buyurtma berish uchun ushbu buyruqni\n /{my_orders}\nyoki pastdagi menyudan «{make_order}» tugmasini bosing")
    else:
        orders = order_repository.get_active_orders(message.from_user.id)
        
        if(orders.count == 0):
            await message.answer(f"Barcha buyurtmalaringiz yetkazib berilgan")
        else:
            for order in orders:
                await message.answer(f''' <b>📥 BUYURTMA</b>\n\n<b>Buyurtma vaqti: </b>{order.created_at}\n\n<b>Buyurtma soni: </b>{order.numbers} ta\n\n@zamin_water_bot''')


async def clear_state(state: FSMContext) -> None:
    await state.clear()