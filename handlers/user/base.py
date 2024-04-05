from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from commands.slash_commands import registration, aloqa, info
from commands.default_commands import contact, about
from keyboards.default.menu_for_user import user_menu_markup, auth_user_menu_markup
from data.repositories.user_repository import UserRepository
from data.models import User

router = Router()
user_repository = UserRepository()
 

#-------- /START -------#
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


#-------- /INFO -------#
@router.message(F.text == about)
async def command_info_button(message: Message) -> None:
    await send_info(message)
    
@router.message(Command(info))
async def command_info_menu(message: Message) -> None:
    await send_info(message)

async def send_info(message: Message):
    await message.answer("<b>Zamin Water - tabiiy ichimlik suvi</b>\n\n💠 Tabiiy tog' suvi\n💠 10 bosqichli filtrda tozalangan\n💠 Uyingiz va ofisingiz uchun eng ma'qul\n🚗 Yetkazib berish mutlaqo <b>BEPUL</b>\n\n<b>💎 19 litr - 10.000 so'm</b>\n\n@mumtaz_suv_bot orqali oson buyurtma bering")


#-------- /ALOQA -------#
@router.message(F.text == contact)
async def command_contact_button(message: Message) -> None:
    await send_contact(message)

@router.message(Command('aloqa'))
async def command_contact_menu(message: Message) -> None:
    await send_contact(message)

async def send_contact(message: Message):
    await message.answer("<b>Barcha viloyatlar uchun yagona ishonch telefoni:</b>\n\n📞 +998555008686 ")


#-------- /SOZLAMALAR -------#
@router.message(Command('sozlamalar'))
async def command_settings_menu(message: Message) -> None:
    await message.answer("⚙️ Hozircha ma'lumotlarni o'zgartirishning imkoni yo'q")
