from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

command_find_article = "Получить информацию по товару"
command_stop_notifications = "Остановить уведомления"
command_get_latest_entires = "Получить информацию из БД"
command_back_to_menu = "Меню"

command_subscribe = "Подписаться"

inline_main_keyboard = [
    [InlineKeyboardButton(text=command_find_article, callback_data="find_article")],
     [InlineKeyboardButton(text=command_get_latest_entires, callback_data="get_latest_entries")],
     [InlineKeyboardButton(text=command_stop_notifications, callback_data="unsubscribe")],
]

default_menu_keyboard = [
    [KeyboardButton(text=command_find_article)],
    [KeyboardButton(text=command_get_latest_entires)],
    [KeyboardButton(text=command_stop_notifications)],
]


subscribe_keyboard = [
    [InlineKeyboardButton(text=command_subscribe, callback_data="subscribe")]
]
subscribe_menu = InlineKeyboardMarkup(inline_keyboard=subscribe_keyboard)

default_menu = ReplyKeyboardMarkup(keyboard=default_menu_keyboard)
menu = InlineKeyboardMarkup(inline_keyboard=inline_main_keyboard)


greet = "Привет, {name}, это тестовый бот. Создатель @AVCAMID!"
