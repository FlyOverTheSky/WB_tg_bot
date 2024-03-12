import asyncio
import json
import os

import requests
from aiogram import F, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import engine
from database.models import ArticleRequest
from keyboards import menu, command_back_to_menu, greet, subscribe_menu, default_menu, command_find_article, \
    command_get_latest_entires
from notifications import start_notification, main_notifications

WB_CARD_API_URL = os.getenv("WB_CARD_API_URL")
TIME_DELAY = int(os.getenv("TIME_DELAY", 5))

dp = Dispatcher()

wb_api_url_params = {
    "appType": 1,
    "curr": "rub",
    "dest": -1257786,
    "spp": 30,
}

current_task_notifications = None


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text=greet.format(name=message.from_user.full_name),
        reply_markup=menu
    )


@dp.message(F.text == command_back_to_menu)
async def back_to_menu_handler(message: Message) -> None:
    await message.answer(
        text="Главное меню",
        reply_markup=menu
    )


@dp.callback_query(F.data == "subscribe")
async def start_notifications_handler(callback_query: CallbackQuery) -> None:
    global current_task_notifications
    current_task_notifications = asyncio.create_task(
        start_notification(
            interval_sec=TIME_DELAY,
            coro_name=main_notifications,
            message=callback_query.message,
        )
    )


@dp.message(F.text == "Остановить уведомления")
@dp.callback_query(F.data == "unsubscribe")
async def stop_notifications_handler(message) -> None:
    global current_task_notifications
    if isinstance(message, CallbackQuery):
        message = message.message

    if current_task_notifications:
        current_task_notifications.cancel()
        answer = "Теперь уведомление об этом артикуле не будут приходить"
    else:
        answer = "Вы не подписаны на артикул."

    await message.answer(
        text=answer,
        reply_markup=default_menu
    )


@dp.message(F.text == "Получить информацию по товару")
@dp.callback_query(F.data == "find_article")
async def input_article_to_find_handler(message) -> None:
    """"Handler для нажатия кнопки поиска по артикулу"""
    if isinstance(message, CallbackQuery):
        message = message.message

    await message.answer(
        text="Введите артикул"
    )


@dp.message(F.text == "Получить информацию из БД")
@dp.callback_query(F.data == "get_latest_entries")
async def get_latest_entries_handler(message) -> None:
    """"Handler для получения последних запросов"""
    if isinstance(message, CallbackQuery):
        message = message.message

    await message.answer(
        text="Последние запросы:"
    )

    async with AsyncSession(engine) as session:
        latest_entries = await session.scalars(
            select(ArticleRequest).limit(5).order_by(desc(ArticleRequest.request_datetime))
        )

    for entire in latest_entries:
        await message.answer(
            text=f"Запрос: №{entire.id}"
                 f"\nПользователь: {entire.user_id}"
                 f"\nАртикул: {entire.article}"
                 f"\nДата: {entire.request_datetime}",
            reply_markup=default_menu
        )


@dp.message(F.text.regexp(r'\d{8}'))
async def find_article_handler(message: Message):
    """Handler для поиска на WB артикула"""

    try:
        wb_api_url_params["nm"] = int(message.text)
    except ValueError:
        return message.answer(
            text="Неправильный артикул, попробуйте ещё раз!"
        )

    await message.answer(
        text="Артикул принят! Собираю информацию 🔎"
    )

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
    article_data = response_data.get('products')
    if not article_data:
        return message.answer(
            text="Такого артикула не было найдено на сайте Wildberries!"
        )
    article_data = article_data[0]

    # Подсчет остатков на всех складах
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
        text=result_message,
        reply_markup=subscribe_menu
    )
