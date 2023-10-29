from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.defoult_btn import menu_btn, phone_btn, get_my_targets_btn
from loader import dp, bot
from data.api import get_my_targets


@dp.message_handler(text="My Targets")
async def my_targets(message: types.Message, state=FSMContext):
    targets = await get_my_targets(message.from_user.id)
    if targets:
        await message.answer("Sizning Targetlariz: ", reply_markup=get_my_targets_btn(targets['user_targets']))
        await state.update_data(targets=targets['user_targets'])
        await state.set_state("get_my_targets")
    else:
        await message.answer("Sizning Targetlariz yo'q", reply_markup=menu_btn)
        
@dp.message_handler(text="🔙 Ortga", state="get_my_targets")
async def my_targets(message: types.Message, state=FSMContext):
    await message.answer("Menu", reply_markup=menu_btn)
    await state.finish()

@dp.message_handler(state="get_my_targets")
async def my_targets(message: types.Message, state=FSMContext):
    data = await state.get_data()
    targets = data["targets"]
    # targets = await get_my_targets(message.from_user.id)
    selected_target = message.text
    if not targets:
        await message.answer("Sizda hali targetlar yo'q")
        return
    tar = "My Target:\n\n"
    for i in targets:
        if selected_target == i['name']:
            tar += f"Nomi: {i['name']}\n"
            tar += f"Tavsifi: {i['description']}\n"
            tar += f"Hafta kunlari: {', '.join(str(a) for a in i['weekday'])}\n"
            tar += f"Boshlanish: {i['start_date']}\n"
            tar += f"Tugash: {i['end_date']}\n"
            tar += f"Vaqt: {i['time']}\n"
            tar += f"Status: {i['status']}\n\n"
            await message.answer(tar)
            break
  
        
    await state.set_state("get_my_targets")
    