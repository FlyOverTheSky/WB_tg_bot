import asyncio

from aiogram.types import Message

from keyboards import default_menu


async def start_notification(interval_sec, coro_name, *args, **kwargs):
    while True:
        await coro_name(*args, **kwargs)
        await asyncio.sleep(interval_sec)


async def main_notifications(message: Message):
    await message.answer(
        text=message.text,
        reply_markup=default_menu,
    )


async def stop_notification(task):
    task.cancel()
