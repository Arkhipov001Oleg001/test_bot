from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from database import sqlite_db
from keyboards.replys import admin_kb
from settings.loader import bot, dp

ID = None


class FsmAdmin(StatesGroup):
    name = State()
    description = State()
    size = State()
    price = State()
    photo = State()
    call_photo = State()
    color = State()
    finish = State()


async def admin(message: types.Message):
    global ID
    ID = message.from_user.id
    await message.reply("Приветствую! Что будем делать?", reply_markup=admin_kb.button_case_admin)
    await message.delete()


async def cm_start(message: types.Message):
    await FsmAdmin.name.set()
    await message.reply('Введите название продукта:')


async def load_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FsmAdmin.next()
    await message.reply('Введите описание продукта:')


async def load_description(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FsmAdmin.next()
    await message.reply('Введите размер:')


async def load_size(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await FsmAdmin.next()
    await message.reply('Укажите стоимость продукта:')


async def load_price(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    await FsmAdmin.next()
    await message.reply('Добавьте фотографию:')


async def load_photo(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        if not'photo' in data.keys():
            data['photo'] = message.photo[0].file_id
        else:
            data['photo'] += '*' + message.photo[0].file_id
    await FsmAdmin.next()
    await message.answer('Хотите добавить ещё фотографию?', reply_markup=InlineKeyboardMarkup().
                        add(InlineKeyboardButton('ДА', callback_data='ДА')).add(InlineKeyboardButton('НЕТ', callback_data='НЕТ')))


async def callback_photo(callback: types.CallbackQuery, state=FSMContext):
    if callback.data == 'ДА':
        await FsmAdmin.photo.set()
        await callback.message.answer('Добавьте фотографию:')
    elif callback.data == 'НЕТ':
        await FsmAdmin.next()
        await callback.message.answer('Укажите цвет:')

async def load_color(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['color'] = message.text
    media_list = []
    for i in data['photo'].split('*')[:-1]:
        new_media = InputMediaPhoto(type='photo', media=i)
        media_list.append(new_media)
    photo_last = InputMediaPhoto(type='photo', media=data['photo'].split('*')[-1], caption=f'{data["name"]}\n'
                                                                                           f'Описание: {data["description"]}\n'
                                                                                           f'Размеры: {data["size"]}\n'
                                                                                           f'Цена: {data["price"]}\n'
                                                                                           f'Цвет: {data["color"]}\n')
    media_list.append(photo_last)
    await FsmAdmin.next()
    await message.answer_media_group(media=media_list)
    await message.answer('Выберите действие', reply_markup=InlineKeyboardMarkup().
                         add(InlineKeyboardButton(text='Добавить в магазин', callback_data='add')).
                         add(InlineKeyboardButton(text='Отмена', callback_data='close')))


async def load_finish(callback: types.CallbackQuery, state=FSMContext):
    if callback.data == 'add':
        await sqlite_db.sql_add_command(state)
        await state.finish()
        await callback.answer('Товар добавлен')
    elif callback.data == 'close':
        await callback.answer('Отмена')


# _______________________________________________________________________________________________________________

async def cancel_handlers(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Всё отменено!')


async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read_2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[-2], f'{ret[0]}\n'
                                                            f'Описание: {ret[1]}\n'
                                                            f'Размеры: {ret[2]}\n'
                                                            f'Цена: {ret[3]}\n'
                                                            f'Цвет: {ret[-1]}\n')
            await message.answer(text='^^^', reply_markup=InlineKeyboardMarkup()
                                 .add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


async def del_callback(callback: types.callback_query):
    await sqlite_db.sql_delete_command(callback.data.replace('del ', ''))
    await callback.answer(text=f'{callback.data.replace("del ", "")} Удалена', show_alert=True)


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(cancel_handlers, commands='отмена', state="*")
    dp.register_message_handler(cancel_handlers, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(admin, commands='загрузить', state=None)
    dp.register_message_handler(cm_start, commands='добавить', state=None)
    dp.register_message_handler(load_name, state=FsmAdmin.name)
    dp.register_message_handler(load_description, state=FsmAdmin.description)
    dp.register_message_handler(load_size, state=FsmAdmin.size)
    dp.register_message_handler(load_price, state=FsmAdmin.price)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FsmAdmin.photo)
    dp.register_callback_query_handler(callback_photo, state=FsmAdmin.call_photo)
    dp.register_message_handler(load_color, state=FsmAdmin.color)
    dp.register_callback_query_handler(load_finish, state=FsmAdmin.finish)
    dp.register_message_handler(delete_item, commands='удалить', state=None)
    dp.register_callback_query_handler(del_callback, lambda x: x.data and x.data.startswith('del '))
