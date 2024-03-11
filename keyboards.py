from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

command_find_article = "Получить информацию по товару"
command_stop_notions = "Остановить уведомления"
command_get_latest_data = "получить информацию из БД"
command_back_to_menu = "Меню"

start_menu = [
    [InlineKeyboardButton(text=command_find_article, callback_data="find_article"),]
]
menu = InlineKeyboardMarkup(inline_keyboard=start_menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

greet = "Привет, {name}, это тестовый бот. Создатель @AVCAMID!"
