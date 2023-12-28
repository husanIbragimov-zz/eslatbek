from aiogram import Dispatcher, types
import asyncio
import aioschedule

async def noon_print():
    print("It's noon!")

async def scheduler():
    aioschedule.every().day.at("12:00").do(noon_print)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())