from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

command_find_article = "Получить информацию по товару"
command_stop_notions = "Остановить уведомления"
command_get_latest_data = "получить информацию из БД"
command_back_to_menu = "Меню"

command_subscribe = "Подписаться"

inline_main_keyboard = [
    [InlineKeyboardButton(text=command_find_article, callback_data="find_article"),
     InlineKeyboardButton(text=command_get_latest_data, callback_data="get_latest_entries"),]
]

back_to_menu_keyboard = [
    [KeyboardButton(text=command_back_to_menu)]
]

subscribe_keyboard = [
    [InlineKeyboardButton(text=command_subscribe, callback_data="subscribe")]
]
subscribe_menu = InlineKeyboardMarkup(inline_keyboard=subscribe_keyboard)

menu = InlineKeyboardMarkup(inline_keyboard=inline_main_keyboard)

back_to_menu = ReplyKeyboardMarkup(keyboard=back_to_menu_keyboard)

greet = "Привет, {name}, это тестовый бот. Создатель @AVCAMID!"
