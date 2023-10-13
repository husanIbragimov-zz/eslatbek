from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.default.defoult_btn import menu_btn
from loader import dp, bot




@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    # user = message.from_user
    # username = user.username if user.username else " "
    # first_name = user.first_name if user.first_name else " "
    # last_name = user.last_name if user.last_name else " "
    # is_active = True
    # create_user(telegram_id=message.from_user.id,
    #             username=username,
    #             first_name=first_name,
    #             last_name=last_name,
    #             is_active = True)
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!", reply_markup=menu_btn)
    
