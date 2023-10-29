from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.default.defoult_btn import menu_btn, phone_btn
from loader import dp, bot
from data.api import create_user, get_me, get_my_targets, get_all_users


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state=FSMContext):
    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}!")
    user = await get_me(message.from_user.id)
    print(user)
    if user == 200:
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
    await state.update_data(age=age)
    await state.set_state("get_phone_number")
    await message.answer("Telefon raqamingizni kiriting", reply_markup=phone_btn)


@dp.message_handler(state="get_phone_number", content_types=types.ContentTypes.CONTACT)
async def get_phone_number(message: types.Message, state=FSMContext):
    try:
        phone_number = message.contact.phone_number
    except:
        await message.answer("Telefon raqamingizni kiriting", reply_markup=phone_btn)
        return

    await state.update_data(phone_number=phone_number)

    data = await state.get_data()

    user = message.from_user
    username = user.username if user.username else " "
    nick_name = user.full_name
    full_name = data["name"]
    age = data["age"]
    is_active = True
    await create_user(telegram_id=message.from_user.id,
                      username=username,
                      nick_name=nick_name,
                      full_name=full_name,
                      age=age,
                      phone_number=phone_number,
                      is_active=is_active)
    await message.answer("Ma'lumotlar saqlandi", reply_markup=menu_btn)
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
