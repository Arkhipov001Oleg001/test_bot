from aiogram import types, Dispatcher
from keyboards.replys import client_kb
from database.sqlite_db import sql_read


# @dp.message_handler(commands=['start', 'help'])
async def start_commands(message: types.Message):
    await message.answer('!!!СТАРТ!!!', reply_markup=client_kb)


# @dp.message_handler(commands=['Режим_работы'])
async def operating_mode(message: types.Message):
    await message.answer('Пн - Чт с 8:00 до 20:00\nПт - Вс с 8:00 до 18:00')
    await message.delete()


# @dp.message_handler(commands=['Расположение'])
async def place_mode(message: types.Message):
    await message.answer('ул.Помидорковая д.4 стр.1')
    await message.delete()


# @dp.message_handler(commands=['Меню'])
async def menu(message: types.Message):
    await sql_read(message)


def register_handler_default(dp: Dispatcher):
    dp.register_message_handler(menu, commands='Меню')
    dp.register_message_handler(start_commands, commands='start')
    dp.register_message_handler(operating_mode, commands='Режим_работы')
    dp.register_message_handler(place_mode, commands='Расположение')
