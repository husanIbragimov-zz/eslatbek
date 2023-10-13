import datetime
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.default.defoult_btn import menu_btn
from keyboards.inline.inline_btn import get_target_btn, choose_weekday_btn, choose_hours_btn, get_calendar


@dp.message_handler(text="weekdays", state=None)
async def weekdays(message: types.Message, state=FSMContext):
    checked = {
        "monday": False,
        "tuesday": False,
        "wednesday": False,
        "thursday": False,
        "friday": False,
        "saturday": False,
        "sunday": False,
        "all_weekdays": False,
    }
    await state.update_data(checked=checked)
    await message.answer("Hafta kunini tanlang", reply_markup=choose_weekday_btn(checked=checked))
    await state.set_state("chose_weekdays")
    

weeks = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
@dp.callback_query_handler(text=weeks, state="chose_weekdays")
async def weekdays(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    checked = data["checked"]
    checked[call.data] = not checked[call.data]
   
    
    await state.update_data(checked=checked)
    
    await call.message.edit_reply_markup(reply_markup=choose_weekday_btn(checked=checked))
    await call.answer(f"{call.data} tanlandi")
    await state.set_state("chose_weekdays")
    
@dp.callback_query_handler(text_contains="all_weekdays", state="chose_weekdays")
async def all_weekdays(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=1)
    data = await state.get_data()
    check = data["checked"]["all_weekdays"]
    if not check:
        checked = {
            "monday": True,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": True,
            "saturday": True,
            "sunday": True,
            "all_weekdays": True,
        }
    else:
        checked = {
            "monday": False,
            "tuesday": False,
            "wednesday": False,
            "thursday": False,
            "friday": False,
            "saturday": False,
            "sunday": False,
            "all_weekdays": False,
        }
        
    # await call.message.answer("Hafta kunini tanlang", reply_markup=choose_weekday_btn(checked=checked))
    await state.update_data(checked=checked)
    await call.message.edit_reply_markup(reply_markup=choose_weekday_btn(checked=checked))
    await state.set_state("chose_weekdays")
    

@dp.callback_query_handler(text="choosen_weekdays", state="chose_weekdays")
async def choosen_weekdays(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    await call.message.answer(data)
    await call.message.delete()
    await call.answer(cache_time=1)
    await call.message.answer("Soatni tanlang", reply_markup=choose_hours_btn())
    await state.set_state("chose_hours")
    

@dp.callback_query_handler(state="chose_hours")
async def choosen_hours(call: types.CallbackQuery, state=FSMContext):
    await call.message.delete()
    hourse = call.data
    await state.update_data(hourse=hourse)
    
    await call.message.answer(f"{hourse} tanlandi")
    await call.answer(cache_time=1)
    await call.message.answer("ok", reply_markup=get_calendar(2023, 10))
    # await state.set_state("chosen_hours")
    
    
    
@dp.message_handler(text="calendar", state=None)
async def calendar(message: types.Message, state=FSMContext):
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    await message.answer("Calendar", reply_markup=get_calendar(year, month))
    await state.update_data(month=month, year=year)
    await state.set_state("calendar_state")

@dp.callback_query_handler(text="previous_month", state="calendar_state")
async def previous_month(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    year = data["year"]
    month = data["month"]
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    await call.message.edit_reply_markup(reply_markup=get_calendar(year, month))
    await state.update_data(month=month, year=year)
    await call.answer(cache_time=1) 
    await state.set_state("calendar_state")
    
@dp.callback_query_handler(text="next_month", state="calendar_state")
async def next_month(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    year = data["year"]
    month = data["month"]
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    await call.message.edit_reply_markup(reply_markup=get_calendar(year, month))
    await state.update_data(month=month, year=year)
    await call.answer(cache_time=1) 
    await state.set_state("calendar_state")
    
    
    

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("select_day"), state="calendar_state")
async def select_day(callback_query: types.CallbackQuery, state=FSMContext):
    await callback_query.answer(cache_time=1)
    
    data = callback_query.data.split("_")
    selected_day = int(data[2])
    selected_month = int(data[3])
    selected_year = int(data[4])

    await bot.send_message(callback_query.from_user.id, f"Tanlangan kun: {selected_day}/{selected_month}/{selected_year}")
    await callback_query.message.delete()
    await callback_query.answer()
    await callback_query.message.answer("Target nomini kiriting")
    await state.set_state("target_name")
    
@dp.message_handler(state="target_name")
async def target_name(message: types.Message, state=FSMContext):
    target_name = message.text
    await state.update_data(target_name=target_name)
    await message.answer(f"{target_name} tanlandi")
    await message.answer("Target haqida ma'lumot kiriting")
    await state.set_state("target_description")
    
    
    