from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_load = KeyboardButton('/Добавить')
button_delete = KeyboardButton('/Удалить')
button_cancel = KeyboardButton('/Отмена')
button_start = KeyboardButton('/start')


button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(button_load).add(button_delete).add(button_cancel).add(button_start)
