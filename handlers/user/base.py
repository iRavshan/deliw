from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from commands.slash_commands import registration
from commands.default_commands import contact, about
from keyboards.default.menu_for_user import user_menu_markup, auth_user_menu_markup
from data.repositories.user_repository import UserRepository
from data.models import User

router = Router()
user_repository = UserRepository()
 
@router.message(CommandStart())
async def command_start(message: Message) -> None:
    user_id = message.from_user.id
    ex_user = user_repository.find_by_id(user_id)
    if(ex_user is None):
        new_user = User(tgId=user_id)
        user_repository.create(new_user)
        await message.answer(f"Siz hali ro'yxatdan o'tmagansiz. Iltimos ro'yxatdan o'tish uchun ushbu buyruqni bosing /{registration}", 
                             reply_markup=user_menu_markup())
    
    elif(ex_user.is_registered is False):
        await message.answer(f"Siz hali ro'yxatdan o'tmagansiz. Iltimos ro'yxatdan o'tish uchun ushbu buyruqni bosing /{registration}",
                             reply_markup=user_menu_markup())
    
    else:
        await message.answer(f"Siz ro'yxatdan o'tgansiz. Marhamat pastdagi tugma orqali buyurtma bering 👇🏻", 
                             reply_markup=auth_user_menu_markup())

@router.message(F.text == about)
async def command_contact(message: Message) -> None:
    await message.answer("<b>MUMTAZ - tabiiy ichimlik suvi</b>\n\n💠 Zam-zam suvi bilan to'yintirilgan\n💠 Tabiiy tog' suvi\n💠 10 bosqichli filtda tozalangan\n💠 Uyingiz va ofisingiz uchun eng ma'qul\n🚗 Yetkazib berish mutlaqo <b>BEPUL</b>\n\n<b>💎 19 litr - 10.000 so'm</b>\n\n@mumtaz_suv_bot orqali oson buyurtma bering")

@router.message(F.text == contact)
async def command_contact(message: Message) -> None:
    await message.answer("<b>Barcha viloyatlar uchun yagona ishonch telefoni:</b>\n\n📞 +998555008686 ")