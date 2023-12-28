from aiogram import executor
import asyncio

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from handlers.users.target_schedule import scheduled

async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(3600)) 
    executor.start_polling(dp, loop=loop, on_startup=on_startup)


