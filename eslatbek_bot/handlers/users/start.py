from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.default.defoult_btn import menu_btn
from loader import dp, bot
from data.api import create_user, get_me, get_my_targets, get_all_users



@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state=FSMContext):
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!")
    user = await get_me(message.from_user.id)
    if user:
        await message.answer("Ma'lumotlarimni o'zgartirish uchun /edit ni bosing", reply_markup=menu_btn)
    else:
        await message.answer("Ro'yxatdan o'tish uchun Ismingizni kiriting: ")
        await state.set_state("get_name")
    
@dp.message_handler(state="get_name")
async def get_name(message: types.Message, state=FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Yoshingizni kiriting")
    await state.set_state("get_age")
    
@dp.message_handler(state="get_age")
async def get_age(message: types.Message, state=FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Yoshingizni raqamda kiriting")
        return
    data = await state.get_data()
    
    user = message.from_user
    username = user.username if user.username else " "
    nick_name = user.full_name 
    full_name = data["name"]
    is_active = True
    await create_user(telegram_id=message.from_user.id,
                username=username,
                nick_name=nick_name,
                full_name=full_name,
                is_active = is_active)
    await message.answer("Ma'lumotlar saqlandi", reply_markup=menu_btn)
    await state.finish()
    
@dp.message_handler(text="My Targets", state=None)
async def my_targets(message: types.Message, state=FSMContext):
    targets = await get_my_targets(message.from_user.id)
    if not targets:
        await message.answer("Sizda hali targetlar yo'q")
        return
    tar = "My Targets:\n\n"
    for i in targets:
        tar += f"Nomi: {i['name']}\n"
        tar += f"Tavsifi: {i['description']}\n"
        tar += f"Boshlanish: {i['start_date']}\n"
        tar += f"Tugash: {i['end_date']}\n"
        tar += f"Status: {i['status']}\n\n"
    await message.answer(tar, reply_markup=menu_btn)
    await state.finish()
    
        
    await message.answer("My Targets")
    await state.finish()
    

    
@dp.message_handler(text="Ma'lumotlarimni o'zgartirish", state=None)
async def edit(message: types.Message, state=FSMContext):
    await message.answer("Ma'lumotlarimni o'zgartirish")
    await state.finish()
    
@dp.message_handler(text="Foydali Linklar", state=None)
async def links(message: types.Message, state=FSMContext):
    await message.answer("Foydali Linklar")
    await state.finish()
    
@dp.message_handler(text="Foydali Kitoblar", state=None)
async def books(message: types.Message, state=FSMContext):
    await message.answer("Foydali Kitoblar")
    await state.finish()
    
@dp.message_handler(text="🔙 Ortga", state="*")
async def back(message: types.Message, state=FSMContext):
    await message.answer("Menu", reply_markup=menu_btn)
    await state.finish()
    
    
    
    
