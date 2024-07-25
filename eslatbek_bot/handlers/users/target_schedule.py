from aiogram import Dispatcher, types
import asyncio
from data.api import get_scheduler_targets, get_one_target
from loader import bot
# import aioschedule



async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        await some_function()


async def some_function():
    targets = await get_scheduler_targets()
    for target in targets:
        txt = f"🔘 <b>Hurmatli do'stim.</b> \n\nSizning <b><i>{target['name']}</i></b> maqsadingiz uchun harakat boshlash vaqti yaqinlashdi.\n Vaqt: {target['time']}."
        try:
            await bot.send_message(chat_id=target["user_id"], text=txt)
        except:
            tar = await get_one_target(target['id'])
            # print(tar)
            await bot.send_message(chat_id=int(tar.get('user')), text=txt)
            # await bot.send_message(chat_id=973108256, text=f"id: {target['id']} - egasini telegram idsiga yuborolmadim")
        # await bot.send_message(chat_id=, text=target["name"])

