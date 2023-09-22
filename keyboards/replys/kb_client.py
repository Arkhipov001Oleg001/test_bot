from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Меню')


client_kb = ReplyKeyboardMarkup(resize_keyboard=True)
client_kb.add(b1).insert(b2).add(b3)
