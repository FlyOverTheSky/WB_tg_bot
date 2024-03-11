import asyncio
import json

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import logging

from pprint import pprint

import requests

import sys

from os import getenv

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database.engine import engine, create_db
from database.models import ArticleRequest
from keyboards import greet, menu, command_back_to_menu

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
WB_CARD_API_URL = getenv("WB_CARD_API_URL")

dp = Dispatcher()

wb_api_url_params = {
    "appType": 1,
    "curr": "rub",
    "dest": -1257786,
    "spp": 30,
}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text=greet.format(name=message.from_user.full_name),
        reply_markup=menu
    )


@dp.message(F.text == command_back_to_menu)
async def back_to_menu_handler(message: types.Message) -> None:
    await message.answer(
        text="Главное меню",
        reply_markup=menu
    )


@dp.callback_query(F.data == "find_article")
async def input_article_to_find_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """"Handler для нажатия кнопки """
    await callback_query.message.answer(
        text="Введите артикул"
    )


@dp.message(F.text.regexp(r'\d{8}'))
async def find_article_handler(message: types.Message):
    """Handler для поиска на WB артикула"""
    await message.answer(
        text="Артикул принят! Собираю информацию 🔎"
    )

    wb_api_url_params["nm"] = int(message.text)
    wb_response = requests.get(
        url=WB_CARD_API_URL,
        params=wb_api_url_params)
    response_data = json.loads(wb_response.content).get('data')

    # Поиск в ответе элемента данных с сайта WB.
    if not response_data:
        return message.answer(
            text="Возникла ошибка с внешним API, пожалуйста сообщите @AVCAMID"
        )

    # Поиск в ответе элемента с товаром
    article_data = response_data.get('products')[0]
    if not article_data:
        return message.answer(
            text="Такого артикула не было найдено на сайте Wildberries!"
        )

    item_stocks = 0
    for size in article_data.get('sizes'):
        for stock in size.get('stocks'):
            item_stocks += stock.get('qty')

    # Деление на 100 у цен, тк приходят цены в копейках.
    search_result = {
        "item_name": article_data.get('name'),
        "item_article": message.text,
        "item_price": article_data.get('priceU') / 100,
        "item_saleprice": article_data.get('salePriceU') / 100,
        "item_rating": article_data.get('reviewRating'),
        "item_stocks": item_stocks
    }

    # Создание асинхронной сессии для сохранения запроса в БД
    async with AsyncSession(engine) as session:
        new_article = ArticleRequest(
            user_id=message.from_user.id,
            article=message.text,
        )
        session.add(new_article)
        await session.commit()

    # Формирование сообщения для пользователя
    result_message = (
        f"Наименование: {search_result["item_name"]}"
        f"\nАртикул: {search_result["item_article"]}"
        f"\nЦена без скидки {search_result["item_price"]}"
        f"\nЦена со скидкой: {search_result["item_saleprice"]}"
        f"\nРейтинг товара: {search_result["item_rating"]}"
        f"\nОсталость товара: {search_result["item_stocks"]}"
        f"\nСсылка на товар: https://www.wildberries.ru/catalog/{message.text}/detail.aspx"
        )

    await message.answer(
        text=result_message
    )


async def main() -> None:
    await create_db()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
